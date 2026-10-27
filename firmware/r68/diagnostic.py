"""MicroPython input/LED bench diagnostic. Does not transmit camera commands.

Use only with the R6.8 proposed 3.3V shift-register harness, no church cables.
Never rename as automatic boot main.py before independent electrical review.
"""
from machine import Pin, ADC
from time import sleep_us, sleep_ms, ticks_ms, ticks_diff
from pins import *

de=Pin(RS_ENABLE,Pin.OUT,value=0)
clk=Pin(CLOCK,Pin.OUT,value=0)
load=Pin(LOAD_N,Pin.OUT,value=1)
di=Pin(INPUT_DATA,Pin.IN)
do=Pin(LED_DATA,Pin.OUT,value=0)
latch=Pin(LED_LATCH,Pin.OUT,value=0)
axes=[ADC(p) for p in ADC_PINS]

def led_write(mask=0):
    if mask < 0 or mask & ~0x3fff1fff: raise ValueError('unassigned LED bit')
    for bit in range(31,-1,-1):
        do.value((mask>>bit)&1)
        clk.value(0);sleep_us(1);clk.value(1);sleep_us(1)
    clk.value(0);latch.value(1);sleep_us(1);latch.value(0)

def read_inputs():
    clk.value(0);load.value(0);sleep_us(2);load.value(1);sleep_us(2)
    result=[]
    for _ in range(INPUT_BITS):
        result.append(di.value())
        clk.value(1);sleep_us(1);clk.value(0);sleep_us(1)
    return result

def run():
    # Shared shift clocks change the hidden 595 shift register while reading.
    # Only led_write pulses LED_LATCH. Reload a complete 32-bit word each time.
    led_write(0)
    last=ticks_ms()
    print('R6.8 DIAGNOSTIC: all camera drivers held disabled')
    try:
        while True:
            bits=read_inputs()
            values=[a.read_u16() for a in axes]
            if ticks_diff(ticks_ms(),last)>=100:
                print('adc',values,'raw_low_bits',[i for i,b in enumerate(bits) if b==0])
                last=ticks_ms()
            sleep_ms(1)
    finally:
        de.value(0);led_write(0)

if __name__=='__main__':run()
