"""Platform-independent R9 controls and protocol transport policy."""
from pins import INPUT, LED

STOP = ("PAN_TILT_STOP", "ZOOM_STOP", "FOCUS_STOP")
CAMERAS = tuple("CAM%d" % n for n in range(1, 5))
SPEEDS = ("SLOW","MIDDLE","FAST")

class Controls:
    def __init__(self, debounce_ms=10):
        self.debounce_ms = debounce_ms
        self.raw = self.stable = 0
        self.changed = [0] * len(INPUT)
        self.phases = [0] * 3
        self.quarters = [0] * 3
        self.invalid_transitions = 0
        self.phase_initialized = False
        self.phase_bits = [(INPUT.index(name+"_A"), INPUT.index(name+"_B"))
                           for name in ("FOCUS","IRIS","MENU")]

    def sample(self, word, now):
        pressed = ~word & ((1 << len(INPUT))-1)
        changes = self.raw ^ pressed
        self.raw = pressed
        down = []
        for i,name in enumerate(INPUT):
            if name == "SPARE_TIE_HIGH" or name.endswith(("_A","_B")):
                continue
            bit = 1 << i
            if changes & bit:
                self.changed[i] = now
            if ((pressed ^ self.stable) & bit
                    and now-self.changed[i] >= self.debounce_ms):
                self.stable ^= bit
                if pressed & bit:
                    down.append(name)
        turns = [0,0,0]
        # Gray states 00 -> 01 -> 11 -> 10 -> 00.
        gray = (0,1,3,2)
        for i,(a,b) in enumerate(self.phase_bits):
            new = gray.index(((pressed >> a)&1) | (((pressed >> b)&1)<<1))
            diff = (new-self.phases[i]) & 3
            self.phases[i] = new
            if not self.phase_initialized:
                continue
            if diff == 2:
                self.invalid_transitions += 1
                self.quarters[i] = 0
            elif diff:
                self.quarters[i] += 1 if diff == 1 else -1
                if abs(self.quarters[i]) == 4:
                    turns[i] = self.quarters[i]//4
                    self.quarters[i] = 0
        self.phase_initialized = True
        return down, turns

def lamp_word(keys):
    return sum(1 << i for i,key in enumerate(LED)
               if key != "UNUSED_OFF" and key in keys)

def axis_value(sample, cal):
    low, middle, high = cal
    if not (0.08 < low < middle < high < 0.92):
        raise ValueError("Invalid calibration; measure endpoints and neutral")
    if sample < 0.055 or sample > 0.945:
        raise ValueError("ADC outside wiring envelope")
    delta = sample-middle
    if abs(delta) <= 0.035:
        return 0.0
    scale = high-middle if delta>0 else middle-low
    return max(-1.0,min(1.0,delta/scale))

class Operator:
    def __init__(self):
        self.selected = None
        self.speed = "SLOW"
        self.armed = False
        self.store = False
        self.fault = None
        self.neutral_since = None
        self.last_vector = (0,0,0)

    def trip(self, cause):
        self.armed = False
        self.store = False
        self.fault = cause
        self.neutral_since = None
        self.last_vector = (0,0,0)
        return [(self.selected,s) for s in STOP] if self.selected else []

    def arm(self, neutral, now):
        if not neutral:
            self.neutral_since = None
            return False
        if self.neutral_since is None:
            self.neutral_since = now
            return False
        if self.selected and now - self.neutral_since >= 500:
            self.armed = True
            self.fault = None
        return self.armed

    def motion(self, samples, calibration, now):
        """Map three measured axes to logical intent. No camera bytes are emitted."""
        try:
            axes = tuple(axis_value(raw, cal) for raw,cal in zip(samples,calibration))
            if len(samples) != 3 or len(calibration) != 3:
                raise ValueError("expected three axes")
        except (TypeError, ValueError):
            return self.trip("ADC WIRING OR CALIBRATION")
        if not self.armed and not self.arm(not any(axes),now):
            return []
        cap = {"SLOW":30,"MIDDLE":65,"FAST":100}[self.speed]
        vector = tuple(round(cap*a) for a in axes)
        if vector == self.last_vector:
            return []
        self.last_vector = vector
        pan,tilt,zoom = vector
        return [(self.selected,("PAN_TILT",pan,tilt) if pan or tilt else "PAN_TILT_STOP"),
                (self.selected,("ZOOM",zoom) if zoom else "ZOOM_STOP")]

    def turn(self, counts):
        if not self.armed:
            return []
        return [(self.selected,(name,count)) for name,count in
                zip(("FOCUS","IRIS","MENU_LOCAL"),counts) if count]

    def keypress(self, keys):
        camera = [k for k in keys if k.startswith("CAM")]
        speeds = [k for k in keys if k in SPEEDS]
        presets = [k for k in keys if k.startswith("PRESET")]
        if len(camera)>1 or len(speeds)>1 or len(presets)>1 or ("STORE" in keys and presets):
            return self.trip("conflicting keys")
        if camera:
            if camera[0] not in CAMERAS:
                return self.trip("IP CAMERA UNAVAILABLE")
            if camera[0] != self.selected:
                stops = self.trip("SELECTED; ARM AT NEUTRAL")
                self.selected = camera[0]
                return stops
        if speeds:
            self.speed = speeds[0]
        if not self.armed:
            return []
        if "STORE" in keys:
            self.store = not self.store
        if presets:
            command = ("PRESET_STORE" if self.store else "PRESET_RECALL",int(presets[0][6:]))
            self.store = False
            return [(self.selected,command)]
        return [(self.selected,k) for k in keys if k in ("AUTO_FOCUS","AUTO_IRIS")]

class Replies:
    """One request per physical port; a fault requires an explicit quiet reset."""
    def __init__(self, address=1):
        if not 1 <= address <= 7:
            raise ValueError("VISCA address out of range")
        self.sender = 0x80 | (address<<4)
        self.frame = bytearray()
        self.pending = None
        self.ack_socket = None
        self.fault = None

    def begin(self, now, timeout=200):
        if self.pending is not None or self.fault:
            raise RuntimeError("port busy or fault latched")
        self.pending = now+timeout
        self.ack_socket = None

    def reset_after_quiet(self):
        self.frame = bytearray()
        self.pending = self.ack_socket = self.fault = None

    def fail(self, cause):
        self.pending = None
        self.fault = cause
        return cause

    def poll(self, now):
        if self.pending is not None and now >= self.pending:
            return self.fail("timeout")
        return None

    def receive(self, data, now):
        if self.poll(now):
            return ["timeout"]
        events = []
        for byte in data:
            if byte != 0xff:
                if len(self.frame)>=15:
                    self.frame = bytearray()
                    return events+[self.fail("oversize reply")]
                self.frame.append(byte)
                continue
            frame = self.frame
            self.frame = bytearray()
            if len(frame)<2 or frame[0]!=self.sender or self.pending is None:
                return events+[self.fail("unexpected reply")]
            kind,socket = frame[1]&0xf0,frame[1]&0x0f
            if kind==0x40 and len(frame)==2 and socket in (1,2) and self.ack_socket is None:
                self.ack_socket = socket
                events.append("ack")
            elif kind==0x50 and len(frame)==2 and self.ack_socket==socket:
                self.pending = self.ack_socket = None
                events.append("complete")
            elif kind==0x60:
                return events+[self.fail("camera error")]
            else:
                return events+[self.fail("unexpected socket or reply type")]
        return events
