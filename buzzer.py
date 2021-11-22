from machine import Pin
from time import sleep

buzzer = Pin(33, Pin.OUT, value = 0)

def buzzer_set():
    buzzer.value(1)

def buzzer_clear():
    buzzer.value(0)
    
    