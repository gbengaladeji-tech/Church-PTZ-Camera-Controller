"""R6.8 offline reference core. No I/O and no claim of camera qualification."""

INPUTS = tuple(["CAM%d" % n for n in range(1, 11)] +
               ["PRESET%d" % n for n in range(1, 13)] +
               ["SLOW", "MIDDLE", "FAST", "AUTO_FOCUS", "AUTO_IRIS", "STORE",
                "FOCUS_A", "FOCUS_B", "IRIS_A", "IRIS_B", "MENU_A", "MENU_B"])
LEDS = INPUTS[:27]
INPUT_INDEX = {name: i for i,name in enumerate(INPUTS[:10])}
INPUT_INDEX.update({name: 10+i for i,name in enumerate(('SLOW','MIDDLE','FAST','FOCUS_A','FOCUS_B','IRIS_A','IRIS_B'))})
INPUT_INDEX.update({'PRESET%d'%n: 23+n for n in range(1,13)})
INPUT_INDEX.update({'AUTO_FOCUS':36,'AUTO_IRIS':37,'STORE':38,'MENU_A':39,'MENU_B':40})
LED_INDEX = {'CAM%d'%n:n-1 for n in range(1,11)}
LED_INDEX.update({'SLOW':10,'MIDDLE':11,'FAST':12})
LED_INDEX.update({'PRESET%d'%n:15+n for n in range(1,13)})
LED_INDEX.update({'AUTO_FOCUS':28,'AUTO_IRIS':29})
LED_ALLOWED_MASK = sum(1<<i for i in LED_INDEX.values())
PINS = {"cam1_tx": 0, "cam1_rx": 1, "cam2_tx": 2, "cam2_rx": 3,
        "display_tx": 4, "display_rx": 5, "cam3_tx": 6, "cam3_rx": 7,
        "cam4_tx": 8, "cam4_rx": 9, "clock": 10, "load_n": 11,
        "input_data": 12, "led_data": 13, "led_latch": 14,
        "rs_enable": 15, "pan_adc": 26, "tilt_adc": 27, "zoom_adc": 28}

def stop_bundle(address=1):
    if address not in range(1, 8):
        raise ValueError("VISCA address must be 1..7")
    h = 0x80 + address
    return (bytes([h, 1, 6, 1, 1, 1, 3, 3, 255]),
            bytes([h, 1, 4, 7, 0, 255]), bytes([h, 1, 4, 8, 0, 255]))

def preset_packet(number, store=False, address=1):
    if not 1 <= number <= 12 or not 1 <= address <= 7:
        raise ValueError("preset 1..12, address 1..7 required")
    # Provisional zero-based mapping; installed profile must prove pp=0..11.
    return bytes([0x80 + address, 1, 4, 0x3f, 1 if store else 2, number-1, 255])

def led_serial_bits(mask):
    if mask < 0 or mask & ~LED_ALLOWED_MASK:
        raise ValueError("only 27 LED positions are assigned")
    # U1 nearest MCU uses Q0..Q7 = LEDs 0..7. Send farthest bit first.
    return tuple((mask >> n) & 1 for n in range(31, -1, -1))

def decode_inputs(raw):
    if len(raw) != 48 or any(v not in (0, 1) for v in raw):
        raise ValueError("exactly 48 binary samples required")
    # First sample is U1 H, then G..A, then U2 H..A.
    return {name: raw[i] == 0 for name,i in INPUT_INDEX.items()}

class Quadrature:
    """Counts valid Gray transitions; four edges per reported detent by default."""
    def __init__(self, initial=3, edges_per_detent=4):
        self.previous = initial
        self.accumulated = 0
        self.errors = 0
        self.edges_per_detent = edges_per_detent

    def update(self, state):
        if state not in (0, 1, 2, 3):
            raise ValueError("two-bit state required")
        p = self.previous
        self.previous = state
        if p == state:
            return 0
        if p ^ state == 3:
            self.errors += 1
            self.accumulated = 0
            return 0
        order = (0, 1, 3, 2)
        delta = 1 if (order.index(state) - order.index(p)) % 4 == 1 else -1
        self.accumulated += delta
        if abs(self.accumulated) >= self.edges_per_detent:
            result = 1 if self.accumulated > 0 else -1
            self.accumulated = 0
            return result
        return 0

class Guard:
    """Faults latch. Stop packets are requests, never proof of physical rest.

    'confirmed_rest' is an explicit external observation after qualification;
    an ACK alone must not set it. Caller supplies monotonically increasing ms.
    """
    def __init__(self, timeout_ms=100, neutral_ms=500):
        self.camera = 1
        self.addresses = (1, 1, 1, 1)
        self.armed = False
        self.fault = "NOT_COMMISSIONED"
        self.timeout_ms = timeout_ms
        self.neutral_ms = neutral_ms
        self.last_input_ms = None
        self.neutral_since_ms = None
        self.last_ms = None
        self.axes = (32768, 32768, 32768)

    def stops(self):
        return tuple((self.camera, p) for p in stop_bundle(self.addresses[self.camera-1]))

    def trip(self, reason):
        self.armed = False
        self.fault = reason
        self.neutral_since_ms = None
        return self.stops()

    def sample(self, axes, now_ms):
        if self.last_ms is not None and now_ms < self.last_ms:
            return self.trip("CLOCK_INVALID")
        self.last_ms = now_ms
        if len(axes) != 3 or any(not isinstance(x, int) or not 2048 <= x <= 63487 for x in axes):
            return self.trip("ADC_RANGE_OR_WIRE")
        self.last_input_ms = now_ms
        self.axes = tuple(axes)
        neutral = all(abs(x - 32768) <= 2500 for x in axes)
        if neutral and self.neutral_since_ms is None:
            self.neutral_since_ms = now_ms
        if not neutral:
            self.neutral_since_ms = None
        # Repeated explicit stops at neutral are bounded by caller's scheduler.
        return self.stops() if neutral else ()

    def tick(self, now_ms):
        if self.last_ms is not None and now_ms < self.last_ms:
            return self.trip("CLOCK_INVALID")
        self.last_ms = now_ms
        if self.last_input_ms is None or now_ms - self.last_input_ms > self.timeout_ms:
            return self.trip("STALE_INPUT")
        return ()

    def arm(self, now_ms, qualified=False, confirmed_rest=False):
        if self.last_ms is not None and now_ms < self.last_ms:
            return False
        if (not qualified or not confirmed_rest or self.neutral_since_ms is None or
                now_ms - self.neutral_since_ms < self.neutral_ms or
                self.last_input_ms is None or now_ms - self.last_input_ms > self.timeout_ms):
            return False
        self.armed = True
        self.fault = None
        return True

    def select(self, camera):
        if camera not in (1, 2, 3, 4):
            return False, ()
        if camera == self.camera:
            return True, ()
        packets = self.trip("CAMERA_CHANGE_REQUIRES_REARM")
        self.camera = camera
        return True, packets

    def pan_tilt(self, pan, tilt, speed):
        if not self.armed:
            raise RuntimeError("controller is disarmed")
        if pan not in (1, 2, 3) or tilt not in (1, 2, 3) or speed not in range(1, 19):
            raise ValueError("invalid PTR provisional movement parameters")
        h = 0x80 + self.addresses[self.camera-1]
        return self.camera, bytes([h, 1, 6, 1, speed, speed, pan, tilt, 255])
