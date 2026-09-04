#!/usr/bin/env python3
"""Draw the survey probe and emit probe.svg.

It earns its place on the page: two of the opening records have a satellite
drawn through them, and one caption is about exactly that, so the thing that
crosses the console is the thing that ruins the exposures.

    python3 probe.py

Grid is 30 by 16 at one unit per pixel, rendered at 4 screen pixels per unit,
which is why it stays seam free instead of shimmering at odd zoom levels.
"""

import os

import pixel

SITE = os.environ.get("SITE", os.path.dirname(os.path.abspath(__file__)))

INK = {
    "P": "#99CCFF",   # solar panel
    "p": "#7799CC",   # panel cell division
    "B": "#FFCC99",   # bus
    "b": "#99AABB",   # bus shadow
    "D": "#FF9900",   # dish and sensor aperture
    "A": "#FF9966",   # booms, mast, instrument mount
}

# First attempt floated the panels free of the bus with a gap of dead cells
# either side, and the three pieces read as three objects rather than one
# craft. The booms on row 8 are what fixed it. The dish went from a closed ring
# (which read as a hoop) to an open bowl for the same reason: silhouette first.
GRID = [
    "..........D........D..........",
    "..........D........D..........",
    "...........D......D...........",
    "............DDDDDD............",
    ".............AAAA.............",
    "..............AA..............",
    "PPPPPPP.....BBBBBB.....PPPPPPP",
    "PpPpPpP.....BbbbbB.....PpPpPpP",
    "PPPPPPPAAAAABBBBBBAAAAAPPPPPPP",
    "PpPpPpP.....BbbbbB.....PpPpPpP",
    "PPPPPPP.....BBBBBB.....PPPPPPP",
    "............BBBBBB............",
    "............BBBBBB............",
    ".............AAAA.............",
    "............DDDDDD............",
    ".............DDDD.............",
]


def main():
    svg = pixel.render(GRID, INK, "A small survey probe")
    path = os.path.join(SITE, "probe.svg")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg)
    print("probe.svg  %dx%d grid, %d lit cells, %d bytes"
          % (len(GRID[0]), len(GRID), pixel.lit(GRID), os.path.getsize(path)))


if __name__ == "__main__":
    main()
