import math
import board
import neopixel
import time
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL
from random import randint
from colors import colors

PIXEL_COUNT = 256
PIXEL_WIDTH = 32
PIXEL_HEIGHT = 8


def rgb2hex(c):
    return int("0x{:02x}{:02x}{:02x}".format(c[0], c[1], c[2]), 16)


gradients = [
    colors['chartreuse1'],
    colors['chartreuse4'],
    colors['gold1'],
    colors['darkorange'],
    colors['cadmiumorange'],
    0xFF0000
]


class LedVisualizer:
    def __init__(self, **kwargs):
        pixels = neopixel.NeoPixel(
            board.D18, PIXEL_COUNT, brightness=0.10, auto_write=False
        )

        self.buffer = PixelFramebuffer(
            pixels,
            PIXEL_WIDTH,
            PIXEL_HEIGHT,
            rotation=2,
            orientation=VERTICAL,
            reverse_x=True,
            reverse_y=True
        )

    def load_frame(self, frame: list):
        if not frame:
            return

        self.buffer.fill(0x000000)

        for i in range(PIXEL_WIDTH):
            x0, y0 = i, PIXEL_HEIGHT
            x1, y1 = i, PIXEL_HEIGHT-frame[i]

            self.gradient_line(x0, y0, x1, y1)

    def gradient_line(self, x0, y0, x1, y1):
        while y1 < y0:
            self.buffer.pixel(x0, y1, self.calculate_gradient(PIXEL_HEIGHT-y1))
            y1 += 1

    def draw(self):
        self.buffer.display()

    def calculate_gradient(self, ampl):
        i = round((ampl/8)*len(gradients)-1)
        return gradients[i]

    def shutdown(self):
        self.buffer.fill(0x000000)
        self.buffer.display()
