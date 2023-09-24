import board
import neopixel
import time

PIXEL_COUNT = 256

pixels = neopixel.NeoPixel(
    board.D18, PIXEL_COUNT, brightness=0.05, auto_write=False
)


def sleepInMs(ms):
    return time.sleep(ms/1000)


for pixel in range(PIXEL_COUNT):
    pixels[pixel] = (255, 0, 0)
    pixels.show()
    sleepInMs(1)

for pixel in range(PIXEL_COUNT):
    pixels[pixel] = (0, 0, 0)
    pixels.show()
    sleepInMs(1)
