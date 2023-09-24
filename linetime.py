import board
import neopixel
import time
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

PIXEL_COUNT = 256
PIXEL_WIDTH = 32
PIXEL_HEIGHT = 8

CHAR_WIDTH = 5
CHAR_SPACING = 1

pixels = neopixel.NeoPixel(
    board.D18, PIXEL_COUNT, brightness=0.05, auto_write=False
)

pixel_framebuf = PixelFramebuffer(
    pixels,
    PIXEL_WIDTH,
    PIXEL_HEIGHT,
    rotation=2,
    orientation=VERTICAL,
    reverse_x=True,
    reverse_y=True
)


def rgb2hex(c):
    return int("0x{:02x}{:02x}{:02x}".format(c[0], c[1], c[2]), 16)


def line(x0, y0, x1, y1, c):
    print(f'Line from ({x0}, {y0}) to ({x1}, {y1})')
    pixel_framebuf.line(x0, y0, x1, y1, rgb2hex(c))
    pixel_framebuf.display()

    time.sleep(0.05)

    pixel_framebuf.fill(0x000000)
    pixel_framebuf.display()


x0, y0 = 0, 0
x1, y1 = PIXEL_WIDTH-1, PIXEL_HEIGHT-1

while True:
    line(x0, y0, x1, y1, (0, 255, 0))

    if (x0 < PIXEL_WIDTH-1):
        x0 += 1
    elif (y0 < PIXEL_HEIGHT-1):
        y0 += 1
    else:
        x0, y0 = 0, 0

    if (x1 > 0):
        x1 += -1
    elif (y1 > 0):
        y1 += -1
    else:
        x1, y1 = PIXEL_WIDTH-1, PIXEL_HEIGHT-1
