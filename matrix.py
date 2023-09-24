import board
import neopixel
import time
from adafruit_pixel_framebuf import PixelFramebuffer

PIXEL_COUNT = 256
PIXEL_COLS = 32
PIXEL_ROWS = 8

pixels = neopixel.NeoPixel(
    board.D18, PIXEL_COUNT, brightness=0.05, auto_write=False
)

pixel_framebuf = PixelFramebuffer(
    pixels,
    PIXEL_ROWS,
    PIXEL_COLS,
    rotation=2,
    reverse_x=True,
    reverse_y=True
)

# pixel_framebuf.fill(0x0000FF)
# pixel_framebuf.display()

# pixel_framebuf.pixel(0,0, 0x0000FF) #blue
# pixel_framebuf.pixel(7,31, 0xFF0000) #red
# pixel_framebuf.display()

for row in range(PIXEL_ROWS):
    for col in range(PIXEL_COLS):
        pixel_framebuf.pixel(row, col, 0xFF0000)
        pixel_framebuf.display()

for row in range(PIXEL_ROWS):
    for col in range(PIXEL_COLS):
        pixel_framebuf.pixel(row, col, 0x000000)
        pixel_framebuf.display()
