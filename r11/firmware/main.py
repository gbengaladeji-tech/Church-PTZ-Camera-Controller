"""Board startup leaves the shared differential driver electrically disabled."""
from machine import Pin
from pins import GPIO

rs_enable = Pin(GPIO['rs_enable'], Pin.OUT, value=0)
# Explicitly call target.diagnostics() from the REPL during a disconnected bench test.
