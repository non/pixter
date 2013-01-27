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
import sys

# takes values [0-255] and scales them to [0-5]
def scale(n): return n / 43

# encode rgb triples into xterm colors
def getcolor(r, g, b): return 16 + scale(b) + scale(g) * 6 + scale(r) * 36

# display a particular pixel (either RGB or RGBA)
def showpixel(p):
    if len(p) == 4:
        r, g, b, a = p
    else:
        r, g, b, a = p + [255]
    if a == 0:
        sys.stdout.write("\033[0m  ")
    else:
        sys.stdout.write("\033[48;5;%dm  " % getcolor(r, g, b))

# with no args, show how to run the program
if not sys.argv[1:]:
    print "usage: %s IMAGE [IMAGE ...]" % sys.argv[0]
    sys.exit(1)

# render each image
for path in sys.argv[1:]:
    im = Image.open(path)
    x0, y0, w, h = im.getbbox()
    for y in range(y0, h):
        for x in range(x0, w):
            showpixel(im.getpixel((x, y)))
        sys.stdout.write("\033[0m\n")
