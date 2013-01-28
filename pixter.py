#!/usr/bin/python
#
# by Erik Osheim
#
# TODO:
# 1. support other color schemes (e.g. indexed)
# 2. warn/error if image is too big to fit the terminal
# 3. optional bg color
# 4. real alpha blending
# 5. indexed ascii format?

from PIL import Image
import os, subprocess, sys

# takes values [0-255] and scales them to [0-5]
def scale(n): return n / 43

# encode rgb triples into xterm colors
def getcolor(r, g, b): return 16 + scale(b) + scale(g) * 6 + scale(r) * 36

# display a particular pixel (either RGB or RGBA)
def showpixel(p):
    if len(p) == 4:
        r, g, b, a = p
    else:
        r, g, b = p
        a = 255
    if a == 0:
        sys.stdout.write("\033[0m  ")
    else:
        sys.stdout.write("\033[48;5;%dm  " % getcolor(r, g, b))

# represents the terminal screen, to assist with resampling
class Screen(object):
    def __init__(self):
        r, c = subprocess.check_output(['stty', 'size']).split()
        self.cols = int(c) - 1
        self.rows = int(r) - 1
        self.aspect = self.cols * 1.0 / self.rows

    def fixaspect(self, ww, hh):
        aspect = ww * 1.0 / hh
        if aspect < self.aspect:
            cols, rows = int(round(self.rows * aspect * 2)), self.rows
        else:
            cols, rows = self.cols, int(round(self.cols / aspect))
        return cols, rows, 2.0 * ww / cols, 1.0 * hh / rows

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('paths', nargs='+', help='image to be displayed', metavar="PATH")
    args = p.parse_args()

    screen = Screen()

    for path in args.paths:
        try:
            im = Image.open(path)
        except IOError:
            print 'ERROR: could not open %r' % path
            continue
            
        x0, y0, w, h = im.getbbox()
        ww, hh = w - x0, h - y0

        # test if resampling is necessary or not
        if hh > screen.rows or ww > screen.cols:
            cols, rows, cellw, cellh = screen.fixaspect(ww, hh)
            for i in range(0, rows):
                y = round(cellh / 2 + y0 + i * cellh)
                for j in range(0, cols / 2):
                    x = round(cellw / 2 + x0 + j * cellw)
                    showpixel(im.getpixel((x, y)))
                sys.stdout.write("\033[0m\n")
        else:
            for y in range(y0, h):
                for x in range(x0, w):
                    showpixel(im.getpixel((x, y)))
                sys.stdout.write("\033[0m\n")
