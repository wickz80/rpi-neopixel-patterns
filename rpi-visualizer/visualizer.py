#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import threading
import re
import sys
import time
import math
import unicodedata
from collections import deque
from led_visualizer import LedVisualizer

NEOPIXEL_COLUMNS = 32
MAX_CAVA_LEVEL = 96		# a nice multiple of DOT3K_ROW_LEVEL (set at 96)
SLEEP = 0.01		# time to sleep the while True loops (0.01 is good)


class Cava(threading.Thread):  # subclass of threading

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        # our cava command with dot3k-specific setup
        self.command = '/usr/bin/cava -p /home/ditto/rpi-visualizer/cava.conf'
        self.lock = threading.Lock() 
        # only one at a time, avoids catchup / lag
        self.fifo = deque([[[0]*NEOPIXEL_COLUMNS]], maxlen=1)

    def get_output(self):						# can return NoneType (!)
        with self.lock:
            try:
                # return the first and only entry in the deque ...
                return self.fifo.popleft()[0]
            except:
                pass					# ... or fail gracefully

    def run(self):
        try:
            process = os.popen(self.command, mode='r')
            while True:
                time.sleep(SLEEP)
                output = process.readline().rstrip()
                if output:
                    if re.match('0;{NEOPIXEL_COLUMNS}', output):
                        continue 			# skip further processing if matches 'empty' string
                    # matches all digits
                    matched = re.findall('(\d+)', output)
                    if matched and len(matched) == NEOPIXEL_COLUMNS:
                        for i in range(len(matched)):
                            # convert string to integers
                            matched[i] = int(matched[i])
                        with self.lock:
                            self.fifo.append([matched])			# append to deque
        except OSError as error:
            print("Error:", error)
            sys.exit(1)


def main():
    c = Cava()
    c.start()

    led_vis = LedVisualizer()

    # main loop, catch Ctrl+C to exit gracefully
    try:
        while True:
            time.sleep(SLEEP)

            visualiser_frame = c.get_output()

            led_vis.load_frame(visualiser_frame)
            led_vis.draw()

    except KeyboardInterrupt:
        led_vis.shutdown()
        sys.exit(0)


if __name__ == '__main__':
    main()
