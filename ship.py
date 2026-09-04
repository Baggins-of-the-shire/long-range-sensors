#!/usr/bin/env python3
"""Draw a survey cutter and emit ship.svg.

An original craft. Wedge hull, dorsal fin, two engine pods slung under it on
short pylons, facing right. Nothing here is anyone else's ship: the point was
to draw something that reads as a spacecraft at 120 pixels wide without
borrowing a silhouette that already means something.

    python3 ship.py

Not placed on the page. It exists so there is a second craft ready when one is
wanted. To make a third, copy this file, change the grid and the palette.
"""

import os

import pixel

SITE = os.environ.get("SITE", os.path.dirname(os.path.abspath(__file__)))

INK = {
    "H": "#FFCC99",   # hull
    "w": "#99CCFF",   # lit ports
    "D": "#FF9966",   # dorsal fin
    "P": "#99AABB",   # pylon
    "E": "#7799CC",   # engine pod
    "n": "#FF9900",   # exhaust, at the aft end of each pod
}

GRID = [
    "..........DDDD................",
    ".........DDDDDD...............",
    "....HHHHHHHHHHHHHHHHHH........",
    "..HHHHHHHHHHHHHHHHHHHHHHHH....",
    "HHHHHHHHHHHHHHHHHHHHHHHHHHHH..",
    "HHwwHHwwHHwwHHHHHHHHHHHHHHHHH.",
    "HHHHHHHHHHHHHHHHHHHHHHHHHHHH..",
    "..HHHHHHHHHHHHHHHHHHHHHHHH....",
    "....HHHHHHHHHHHHHHHHHH........",
    "...PP........PP...............",
    ".EEEEEE....EEEEEE.............",
    ".nEEEEE....nEEEEE.............",
    ".EEEEEE....EEEEEE.............",
]


def main():
    svg = pixel.render(GRID, INK, "A survey cutter")
    path = os.path.join(SITE, "ship.svg")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg)
    print("ship.svg   %dx%d grid, %d lit cells, %d bytes"
          % (len(GRID[0]), len(GRID), pixel.lit(GRID), os.path.getsize(path)))


if __name__ == "__main__":
    main()
