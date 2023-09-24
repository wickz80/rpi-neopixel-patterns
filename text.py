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


text = input()
offset = len(text) * (CHAR_WIDTH + CHAR_SPACING)

for x in range(PIXEL_WIDTH, -offset, -1):
    pixel_framebuf.fill(0x000000)
    time.sleep(0.05)
    pixel_framebuf.text(text, x, 1, 0xFFFFFF)
    pixel_framebuf.display()
