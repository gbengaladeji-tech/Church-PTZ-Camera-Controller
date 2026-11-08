"""W55RP20 MicroPython target, diagnostic startup with all camera TX disabled."""
import time
import rp2
from machine import Pin, ADC, UART
from pins import GPIO, PIO_IDS
from core import Controls, Operator, lamp_word

@rp2.asm_pio(out_init=rp2.PIO.OUT_HIGH, sideset_init=rp2.PIO.OUT_HIGH,
             out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def tx8n1():
    pull(block).side(1)[7]
    set(x,7).side(0)[7]
    label("bits")
    out(pins,1)
    jmp(x_dec,"bits")[6]

@rp2.asm_pio(in_shiftdir=rp2.PIO.SHIFT_RIGHT)
def rx8n1():
    wait(0,pin,0)
    set(x,7)[11]
    label("bits")
    in_(pins,1)
    jmp(x_dec,"bits")[6]
    in_(pins,1)
    push(noblock)
    wait(1,pin,0)

class PioPort:
    def __init__(self, pair, tx, rx, baud):
        self.tx=rp2.StateMachine(pair[0],tx8n1,freq=8*baud,
                                 out_base=Pin(tx),sideset_base=Pin(tx))
        self.rx=rp2.StateMachine(pair[1],rx8n1,freq=8*baud,
                                 in_base=Pin(rx,Pin.IN,Pin.PULL_UP))
        self.tx.active(1)
        self.rx.active(1)
    def write(self,data):
        for byte in data:
            self.tx.put(byte)
    def read(self):
        out = bytearray()
        while self.rx.rx_fifo():
            word = self.rx.get() >> 23
            if not word & 0x100:
                raise OSError("missing stop bit")
            out.append(word & 0xff)
        return bytes(out)

class Target:
    def __init__(self, baud):
        self.enable=Pin(GPIO["rs_enable"],Pin.OUT,value=0)
        self.clock=Pin(GPIO["clock"],Pin.OUT,value=0)
        self.load=Pin(GPIO["load_n"],Pin.OUT,value=1)
        self.keydata=Pin(GPIO["input_data"],Pin.IN,Pin.PULL_UP)
        self.leddata=Pin(GPIO["led_data"],Pin.OUT,value=0)
        self.latch=Pin(GPIO["led_latch"],Pin.OUT,value=0)
        self.axes=[ADC(GPIO[k]) for k in ("pan_adc","tilt_adc","zoom_adc")]
        self.uart1=UART(0,baudrate=baud,tx=Pin(GPIO["cam1_tx"]),
                        rx=Pin(GPIO["cam1_rx"]), timeout=0,rxbuf=256)
        self.ports=[self.uart1]
        for n,pair in enumerate(PIO_IDS,2):
            self.ports.append(PioPort(pair,GPIO["cam%d_tx"%n],GPIO["cam%d_rx"%n],baud))
        self.display=UART(1,baudrate=9600,tx=Pin(GPIO["display_tx"]),
                          rx=Pin(GPIO["display_rx"]),timeout=0)
        self.baud=baud
        self.lamps(0)

    def safe(self):
        self.enable(0)

    def scan(self):
        self.load(0)
        time.sleep_us(2)
        self.load(1)
        word=0
        for bit in range(48):
            word |= self.keydata() << bit
            self.clock(1)
            self.clock(0)
        return word

    def lamps(self,word):
        for bit in range(31,-1,-1):
            self.leddata((word>>bit)&1)
            self.clock(1)
            self.clock(0)
        self.latch(1)
        self.latch(0)

    def walk_lamps(self, confirm):
        """Illuminate each of the 27 circuits with TX held off."""
        if confirm != "ISOLATED_DUMMY_ONLY":
            raise ValueError("Explicit isolated confirmation required")
        from pins import LED
        self.safe()
        try:
            for bit,name in enumerate(LED):
                if name != "UNUSED_OFF":
                    print(bit,name)
                    self.lamps(1<<bit)
                    time.sleep_ms(600)
        finally:
            self.lamps(0)

    def loopback(self, port, confirm, timeout_ms=100):
        """Physical isolated echo. Confirm removal of ALL camera and LAN cables first."""
        if confirm != "ISOLATED_DUMMY_ONLY" or not 1 <= port <= 4:
            raise ValueError("Explicit isolated-loopback confirmation required")
        data=bytes((0x55,0xA0+port,0x2A,0x00,0xFF))
        for p in self.ports:
            p.read()
        self.enable(1)
        try:
            self.ports[port-1].write(data)
            deadline=time.ticks_add(time.ticks_ms(),timeout_ms)
            received=[bytearray() for _ in self.ports]
            while time.ticks_diff(deadline,time.ticks_ms())>0:
                for n,p in enumerate(self.ports):
                    received[n].extend(p.read() or b"")
                time.sleep_ms(1)
            return received[port-1]==data and all(not v for n,v in enumerate(received,1) if n!=port)
        finally:
            self.safe()

    def diagnostics(self, seconds=15, display_enabled=False, calibration=None):
        self.safe()
        controls=Controls()
        operator=Operator()
        origin=time.ticks_ms()
        end=time.ticks_add(origin,int(seconds*1000))
        try:
            while time.ticks_diff(end,time.ticks_ms())>0:
                now=time.ticks_diff(time.ticks_ms(),origin)
                keys,turns=controls.sample(self.scan(),now)
                actions = operator.keypress(keys) + operator.turn(turns)
                raw = [a.read_u16() for a in self.axes]
                if calibration is not None:
                    actions += operator.motion([v/65535 for v in raw],calibration,now)
                if keys or any(turns) or actions:
                    print(now,keys,turns,raw,operator.fault,"LOCAL INTENT",actions)
                    self.lamps(lamp_word((operator.selected,operator.speed)))

                    if display_enabled:
                        msg='t0.txt="%s"'%(operator.selected or "DIAGNOSTIC")
                        self.display.write(msg.encode()+b"\xff\xff\xff")
                time.sleep_ms(1)
        finally:
            self.lamps(0)
            self.safe()

if __name__ == "__main__":
    Target(38400).diagnostics()
