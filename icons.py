#!/usr/bin/env python3
"""Draw the site icon: the console's own elbow, plus two bar segments.

One geometry, two renderers. `icon.svg` is the favicon modern browsers prefer
and stays sharp at any size; the PNGs exist for the home screen and for the
browsers that still want a raster. Both are built from the numbers below, so
they cannot drift apart.

    python3 icons.py

Deliberately no stars or telescope glyph. At 32 pixels in a browser tab the
elbow and two bars are still legible as a shape; anything finer turns to mush.
"""

import os

from PIL import Image, ImageDraw

SITE = os.environ.get("SITE", os.path.dirname(os.path.abspath(__file__)))

S = 512.0          # design canvas, everything below is in these units
BLACK = "#000000"
MAUVE = "#7799CC"
AMBER = "#FF9900"
TAN = "#FFCC99"

VX0, VX1 = 51.0, 184.0      # vertical arm, left and right edges
HY0, HY1 = 72.0, 185.0      # horizontal arm, top and bottom edges
VY1 = 440.0                 # bottom of the vertical arm
HX1 = 461.0                 # right end of the horizontal arm
R = 96.0                    # outer top-left radius
F = 48.0                    # inner concave fillet
CAP = (HY1 - HY0) / 2.0     # right end of the arm is a semicircle
BOT = (VX1 - VX0) / 2.0     # so is the bottom of the vertical arm

BARS = [                    # x0, y0, x1, y1, colour
    (225.0, 236.0, 461.0, 297.0, AMBER),
    (225.0, 338.0, 369.0, 399.0, TAN),
]


def svg():
    path = (
        "M {vx0},{hy0r} "
        "A {R},{R} 0 0 1 {vx0r},{hy0} "
        "L {hx1c},{hy0} "
        "A {CAP},{CAP} 0 0 1 {hx1c},{hy1} "
        "L {vx1f},{hy1} "
        "A {F},{F} 0 0 0 {vx1},{hy1f} "
        "L {vx1},{vy1b} "
        "A {BOT},{BOT} 0 0 1 {vx0},{vy1b} "
        "Z"
    ).format(vx0=VX0, hy0r=HY0 + R, R=R, vx0r=VX0 + R, hy0=HY0,
             hx1c=HX1 - CAP, CAP=CAP, hy1=HY1, vx1f=VX1 + F, F=F,
             vx1=VX1, hy1f=HY1 + F, vy1b=VY1 - BOT, BOT=BOT)

    bars = "\n".join(
        '  <rect x="{0}" y="{1}" width="{2}" height="{3}" rx="{4}" fill="{5}"/>'.format(
            x0, y0, x1 - x0, y1 - y0, (y1 - y0) / 2.0, colour)
        for x0, y0, x1, y1, colour in BARS)

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" '
        'width="512" height="512" role="img" aria-label="Long Range Sensors">\n'
        '  <rect width="512" height="512" fill="{black}"/>\n'
        '  <path d="{path}" fill="{mauve}"/>\n'
        '{bars}\n'
        '</svg>\n'
    ).format(black=BLACK, path=path, mauve=MAUVE, bars=bars)


def raster(size, inset=1.0):
    """Draw at 4x and downsample. Cheaper than writing an antialiaser, and the
    edges that matter here are one big curve and four pill ends."""
    ss = 4
    n = int(S * ss)
    im = Image.new("RGB", (n, n), BLACK)
    d = ImageDraw.Draw(im)
    k = ss

    # The L, as two rectangles that stop short of where the ends round off,
    # plus a disc at each end. Filling all the way and adding a disc on top
    # leaves the corners square, because the disc is then inside the rect.
    d.rectangle([VX0 * k, HY0 * k, VX1 * k, (VY1 - BOT) * k], fill=MAUVE)
    d.ellipse([VX0 * k, (VY1 - 2 * BOT) * k, VX1 * k, VY1 * k], fill=MAUVE)
    d.rectangle([VX0 * k, HY0 * k, (HX1 - CAP) * k, HY1 * k], fill=MAUVE)
    d.ellipse([(HX1 - 2 * CAP) * k, HY0 * k, HX1 * k, HY1 * k], fill=MAUVE)

    # Outer top-left corner: black the square out, then put the disc quadrant
    # back. What survives is the quarter nearest the inside, which is the round.
    d.rectangle([VX0 * k, HY0 * k, (VX0 + R) * k, (HY0 + R) * k], fill=BLACK)
    d.ellipse([VX0 * k, HY0 * k, (VX0 + 2 * R) * k, (HY0 + 2 * R) * k], fill=MAUVE)

    # Inner concave fillet: mauve square, then bite a disc out of it. What is
    # left is the quarter nearest the corner, which is the curve we want.
    d.rectangle([VX1 * k, HY1 * k, (VX1 + F) * k, (HY1 + F) * k], fill=MAUVE)
    d.ellipse([VX1 * k, HY1 * k, (VX1 + 2 * F) * k, (HY1 + 2 * F) * k], fill=BLACK)

    for x0, y0, x1, y1, colour in BARS:
        d.rounded_rectangle([x0 * k, y0 * k, x1 * k, y1 * k],
                            radius=(y1 - y0) / 2.0 * k, fill=colour)

    if inset < 1.0:
        # Maskable icons get cropped to a circle by the launcher, so pull the
        # artwork into the safe zone rather than letting a corner get shaved.
        small = im.resize((int(n * inset), int(n * inset)), Image.LANCZOS)
        canvas = Image.new("RGB", (n, n), BLACK)
        off = (n - small.width) // 2
        canvas.paste(small, (off, off))
        im = canvas

    return im.resize((size, size), Image.LANCZOS)


def main():
    out = []

    path = os.path.join(SITE, "icon.svg")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg())
    out.append(("icon.svg", os.path.getsize(path)))

    for name, size, inset in [("apple-touch-icon.png", 180, 1.0),
                              ("icon-192.png", 192, 1.0),
                              ("icon-512.png", 512, 1.0),
                              ("icon-maskable-512.png", 512, 0.68)]:
        p = os.path.join(SITE, name)
        raster(size, inset).save(p, "PNG", optimize=True)
        out.append((name, os.path.getsize(p)))

    for name, size in out:
        print("%-26s %6d bytes" % (name, size))


if __name__ == "__main__":
    main()
