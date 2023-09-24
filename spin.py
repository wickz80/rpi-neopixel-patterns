import board
import neopixel
import time
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL
from random import randint

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


start = [
    (0, 0, 1, 1),
    (0, 1, 1, 0),
    (1, 1, 0, 0),
    (0, 1, 1, 0),
]

rotated90 = [
    (0, 1, 0, 0),
    (1, 1, 1, 0),
    (1, 0, 1, 1),
    (0, 0, 0, 1),
]

rot = []
for tup in start[::-1]:
    for num in tup:


objects = []
for _ in range(1):
    position = (randint(0, PIXEL_WIDTH), randint(0, PIXEL_HEIGHT))

    objects.append(
        Square(3,
               position=(1, 1),
               color=0x0000FF,
               delta_x=1,
               delta_y=1
               # delta_x = randint(-2,2),
               # delta_y = randint(-1,1)
               )
    )

while True:
    for obj in objects:
        obj.move(pixel_framebuf)

    pixel_framebuf.display()

    time.sleep(0.2)
