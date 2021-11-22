from machine import Pin
import neopixel

n = 12
p = 15

np = neopixel.NeoPixel(Pin(p), n)

def clear():
    for i in range(n):
        np[i] = (0, 0, 0)
        np.write() 
        
def set_color(r, g, b):
    for i in range(n):
        np[i] = (r, g, b)
    np.write()
    
def bounce(r, g, b, wait):
    for i in range(4 * n):
        for j in range(n):
            np[j] = (r, g, b)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(wait)
        