import time
import network
import json
from neopixel import NeoPixel
from machine import Pin, SPI, SoftSPI

numpix = 12 # number of led's
neopin = Pin(0, Pin.OUT)  # GPIO0
pixels = NeoPixel(neopin, numpix)


def demo(np):
    n = np.n

    # cycle
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)

    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

    # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        np.write()

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()

def set_neopixel_color(np,val):
    n = np.n
    value = val
    
    rgb = [0, 0, 0]
    
    if value <= 0:
        rgb[0] = 0
        rgb[1] = 255
        rgb[2] = 0
    else:
        if value <= 1:
            rgb[0] = 153
            rgb[1] = 204
            rgb[2] = 0 
        else:
            if value <= 2:
                rgb[0] = 255
                rgb[1] = 255
                rgb[2] = 153
            else:
                if value <= 3:
                    rgb[0] = 153
                    rgb[1] = 204
                    rgb[2] = 0
                else:
                    if value <= 4:
                        rgb[0] = 255
                        rgb[1] = 204
                        rgb[2] = 0
                    else:
                        if value <= 5:
                            rgb[0] = 255
                            rgb[1] = 153
                            rgb[2] = 0
                        else:
                            if value <= 6:
                                rgb[0] = 255
                                rgb[1] = 102
                                rgb[2] = 0
                            else:
                                if value <= 7:
                                    rgb[0] = 255
                                    rgb[1] = 0
                                    rgb[2] = 0
                                else:
                                    if value > 7:
                                        rgb[0] = 255
                                        rgb[1] = 0
                                        rgb[2] = 255
    # Set all LEDs to the same color
    print(rgb[0],rgb[1],rgb[2])
    for i in range(n):
        np[i] = (int(rgb[0]), int(rgb[1]), int(rgb[2]))
    np.write()
 
yellow = (255, 100, 0)
orange = (255, 50, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
color0 = red
none = (0,0,0,0)

pixels.fill(none)
#pixels.set_pixel_line_gradient(3, 13, green, blue)
#pixels.set
# _pixel_line(14, 16, red)
#pixels.set_pixel(20, (255, 255, 255))
#pixels[0] = (255, 0, 0, 10)
#pixels[1] = (0, 255, 0, 10)
#pixels[2] = (0, 0, 255, 10)
#pixels[3] = (255, 0, 0, 50)
#pixels[4] = (0, 255, 0, 50)
#pixels[5] = (0, 0, 255, 50)
pixels.write()
time.sleep(5)
print(pixels.n)
demo(pixels)

