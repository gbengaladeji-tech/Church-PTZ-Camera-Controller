"""Experimental MicroPython 8N1 PIO transport for logic-analyser loopback ONLY.

No camera profile, no hardware pass claimed. Frame errors are not detected by
this minimal receiver, which is a commissioning blocker for camera use.
Uses six state machines: TX/RX pairs 0/1, 2/3, 4/5. This is a small proposed
PIO serial implementation; it is not a copy of a qualified board UART driver.
Reference for assembler semantics: https://docs.micropython.org/en/latest/library/rp2.html
"""
from machine import Pin
import rp2

@rp2.asm_pio(out_init=rp2.PIO.OUT_HIGH, sideset_init=rp2.PIO.OUT_HIGH,
             out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def tx8n1():
    pull(block).side(1)[7]
    set(x,7).side(0)[7]
    label('bits')
    out(pins,1)
    jmp(x_dec,'bits')[6]

@rp2.asm_pio(in_shiftdir=rp2.PIO.SHIFT_RIGHT)
def rx8n1():
    wait(0,pin,0)
    set(x,7)[10]
    label('bits')
    in_(pins,1)
    jmp(x_dec,'bits')[6]
    push(block)
    wait(1,pin,0)

class PIOUART:
    def __init__(self,tx_sm,rx_sm,tx_pin,rx_pin,baud=38400):
        self.tx=rp2.StateMachine(tx_sm,tx8n1,freq=8*baud,
            out_base=Pin(tx_pin),sideset_base=Pin(tx_pin))
        self.rx=rp2.StateMachine(rx_sm,rx8n1,freq=8*baud,in_base=Pin(rx_pin,Pin.IN,Pin.PULL_UP))
        self.tx.active(1);self.rx.active(1)
    def write(self,data):
        for b in data:self.tx.put(b)
    def read_available(self):
        return bytes([self.rx.get()>>24 for _ in range(self.rx.rx_fifo())])
