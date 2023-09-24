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

buffer = PixelFramebuffer(
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


def rotate_matrix(matrix):
    if not matrix:
        return []

    # Transpose the matrix
    transposed_matrix = [[matrix[j][i] for j in range(
        len(matrix))] for i in range(len(matrix[0]))]

    # Reverse the order of rows to get the 90-degree clockwise rotated matrix
    rotated_matrix = [tuple(row[::-1]) for row in transposed_matrix]

    return rotated_matrix


start = [
    (1, 1, 0, 0),
    (1, 0, 1, 0),
    (0, 1, 0, 1),
    (0, 0, 1, 1),
]

sword = [
    (0, 0, 0, 1, 0, 0, 0),
    (0, 0, 1, 1, 0, 0, 0),
    (0, 0, 1, 1, 0, 0, 0),
    (0, 0, 1, 1, 0, 0, 0),
    (0, 0, 1, 1, 0, 0, 0),
    (0, 0, 1, 1, 0, 0, 0),
    (0, 0, 0, 1, 0, 0, 0),
    (0, 0, 0, 1, 0, 0, 0),
]

apple = [
    (0, 0, 1, 1, 0, 0),
    (0, 1, 1, 1, 1, 0),
    (1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1),
    (0, 1, 1, 1, 1, 0),
    (0, 0, 1, 1, 0, 0),
]
pizza = [
    (1, 1, 1, 1, 1, 1),
    (1, 1, 0, 0, 1, 1),
    (1, 1, 0, 0, 1, 1),
    (1, 1, 1, 1, 1, 1),
    (0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0),
]
hamburger = [
    (0, 0, 1, 1, 0, 0),
    (0, 1, 1, 1, 1, 0),
    (1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1),
    (0, 1, 1, 1, 1, 0),
    (0, 0, 1, 1, 0, 0),
]
ice_cream = [
    (0, 0, 1, 1, 0, 0),
    (0, 1, 1, 1, 1, 0),
    (1, 1, 1, 1, 1, 1),
    (0, 1, 1, 1, 1, 0),
    (0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0),
]
banana = [
    (0, 1, 1, 0, 0, 0),
    (1, 1, 1, 1, 0, 0),
    (1, 1, 1, 1, 0, 0),
    (0, 1, 1, 1, 0, 0),
    (0, 0, 0, 1, 0, 0),
    (0, 0, 0, 1, 0, 0),
]

ocean_waves = [
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,
     0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0,
     0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0,
     0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
     0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
     0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0),
    (0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0),
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0)
]


def fill_custom(custom, buffer: PixelFramebuffer):
    pos = (2, 2)

    for (x, t) in enumerate(custom):
        for (y, v) in enumerate(t):
            if not v:
                continue

            buffer.pixel(x, y, 0xFF00FF)
            buffer.display()


def fill_custom_swap(custom, buffer: PixelFramebuffer):
    pos = (2, 2)

    for (x, t) in enumerate(custom):
        for (y, v) in enumerate(t):
            if not v:
                continue

            buffer.pixel(y, x, 0xFF00FF)
            buffer.display()


def clear():
    buffer.fill(0x000000)
    buffer.display()


shapes = [start, sword, apple, pizza, hamburger, ice_cream, banana]

while True:
    try:
        # for shape in shapes:

        #     fill_custom(shape, buffer)
        #     time.sleep(1)
        #     clear()

        #     fill_custom(rotate_matrix(shape), buffer)
        #     time.sleep(1)
        #     clear()

        fill_custom_swap(ocean_waves, buffer)
        time.sleep(10)
        clear()

    except KeyboardInterrupt:
        buffer.fill(0x000000)
        buffer.display()
        break
