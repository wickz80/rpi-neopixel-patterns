import board
import neopixel
import time
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL
from random import randint

PIXEL_COUNT = 256
PIXEL_WIDTH = 32
PIXEL_HEIGHT = 8

pixels = neopixel.NeoPixel(
    board.D18, PIXEL_COUNT, brightness=0.15, auto_write=False
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


class Square:
    def __init__(self, size, **kwargs):
        self.size = size

        default_kwargs = {
            "position": (0, 0),
            "bounds": (PIXEL_WIDTH, PIXEL_HEIGHT),
            "delta_x": 1,
            "delta_y": 1,
            "color": 0x00FF00,
            "trailing": False,
            # only works with Size = 1
            "edge_hit_ghosting": False
        }
        kwargs = {**default_kwargs, **kwargs}

        # top left corner of square
        self.position = kwargs['position']

        # bounds of matrix
        self.mw, self.mh = kwargs['bounds']

        # initial velocity
        self.delta_x = kwargs['delta_x']
        self.delta_y = kwargs['delta_y']

        self.trailing = kwargs['trailing']
        self.color = kwargs['color']
        self.edge_hit_ghosting = kwargs['edge_hit_ghosting'] and size == 1

    def is_x_collision(self, x):
        return (x < 0 or (x + self.size) > self.mw)

    def is_y_collision(self, y):
        return (y < 0 or (y + self.size) > self.mh)

    def calc_new_position(self, x, y):
        return (x + self.delta_x, y + self.delta_y)

    def move(self, buffer: PixelFramebuffer):
        x0, y0 = self.position
        print(f'curr position: ({x0}, {y0})')

        x1, y1 = self.calc_new_position(x0, y0)
        print(f'new position: ({x1}, {y1})')

        xc, yc = self.is_x_collision(x1), self.is_y_collision(y1)
        if xc or yc:
            if xc:
                self.delta_x = -self.delta_x
            if yc:
                self.delta_y = -self.delta_y
            x1, y1 = self.calc_new_position(x0, y0)

        # clear existing rect
        if not self.trailing:
            self.draw(buffer)

        # draw sq in new position
        self.position = (x1, y1)

        self.draw(buffer, self.color)

    def edge_hit(self, x, y):
        return (x == 0 or y == 0 or (x + self.size) == self.mw or (y + self.size) == self.mh)

    def draw(self, buffer, color=0x000000):
        x, y = self.position

        if self.edge_hit_ghosting and self.edge_hit(x, y):
            color = 0xFFFFFF

        buffer.fill_rect(x, y, self.size, self.size, color)


objects = []
for _ in range(25):
    position = (randint(0, PIXEL_WIDTH), randint(0, PIXEL_HEIGHT))

    objects.append(
        Square(1,
               position=(1, 1),
               color=0x0000FF,
               delta_x=randint(-3, 3),
               delta_y=randint(-2, 2),
               edge_hit_ghosting=True
               )
    )


while True:
    try:
        for obj in objects:
            obj.move(pixel_framebuf)

        pixel_framebuf.display()

        time.sleep(0.1)

    except KeyboardInterrupt:
        pixel_framebuf.fill(0x000000)
        pixel_framebuf.display()
        break
