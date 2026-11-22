"""W55RP20 bench I/O, with no camera packet write path."""
import time
from machine import ADC, Pin, UART
from display import Display
from guard import Session
from pins import GPIO


def diagnostics(seconds=15, calibration=None, *, display_enabled=False, acknowledge_ms=None):
    enable=Pin(GPIO['rs_enable'],Pin.OUT,value=0)
    load=Pin(GPIO['load_n'],Pin.OUT,value=1)
    clock=Pin(GPIO['clock'],Pin.OUT,value=0)
    data=Pin(GPIO['input_data'],Pin.IN,Pin.PULL_UP)
    axes=tuple(ADC(GPIO[name]) for name in ('pan_adc','tilt_adc','zoom_adc'))
    screen=Display()
    uart=None
    if display_enabled:
        uart=UART(1,baudrate=9600,bits=8,parity=None,stop=1,tx=Pin(GPIO['display_tx']),rx=Pin(GPIO['display_rx']),timeout=0)
    state=Session(calibration)
    start=time.ticks_ms()
    acknowledged=False
    last_status=None
    try:
        while (elapsed:=time.ticks_diff(time.ticks_ms(),start))<seconds*1000:
            load(0)
            time.sleep_us(2)
            load(1)
            word=0
            for bit in range(48):
                word |= data()<<bit
                clock(1)
                clock(0)
            samples=tuple(adc.read_u16()/65535 for adc in axes)
            ack=acknowledge_ms is not None and elapsed>=acknowledge_ms and not acknowledged
            if ack:
                acknowledged=True
            commands=state.step(word,samples,elapsed,acknowledge=ack)
            status=(state.fault,state.operator.selected,state.operator.speed,state.operator.armed)
            if commands or status!=last_status:
                print(elapsed,hex(word),samples,status,'LOCAL INTENTS',commands)
                last_status=status
            if uart:
                screen.receive(uart.read() or b'')
                packet=screen.update(elapsed,status[1],status[2],status[0],status[3],preset=state.last_preset)
                if packet:
                    uart.write(packet)
            time.sleep_ms(2)
    finally:
        enable(0)
