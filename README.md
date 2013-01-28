## Pixter

by Erik Osheim

### Description

Pixter is a little toy program for display small images directly in your
terminal using xterm color code sequences and spaces. It uses two space
characters per "pixel" (since most fixed-width fonts are around twice as tall
as wide), and supports 216 (6x6x6 color cube) colors.

Images that are too large for the screen will be resampled to fit.

Possible uses include visual status output from scripts, exciting graphical
error messages, etc.

### Requirements

Pixter requires Python and the Python Imaging Library (PIL).

Your terminal emulator must support xterm colors. Many terminals do (e.g.
xterm, Gnome Terminal, iTerm) but some don't. Sorry.

I have no idea if it's possible to use this on Windows, but I doubt it.

### License

This code is in the public domain.

### Future Work

Only color images are currently supported, and some color modes may not work
(I'm just using PIL's `getpixel` method). True alpha blending isn't supported
(all non-zero alpha values are treated as 255), and it'd be nice to have an
option to set a background color (right now your terminal's default background
color is used).
