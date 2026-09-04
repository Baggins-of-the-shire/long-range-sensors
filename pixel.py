#!/usr/bin/env python3
"""Turn a grid of characters into an SVG of flat rects.

Shared by probe.py and ship.py. Keeping the renderer in one place means the
two craft cannot drift apart in how they are drawn, and a new one is a grid
and a palette rather than another copy of this code.
"""


def check(grid, ink):
    width = len(grid[0])
    for y, row in enumerate(grid):
        if len(row) != width:
            raise SystemExit("row %d is %d wide, expected %d" % (y, len(row), width))
        for ch in row:
            if ch != "." and ch not in ink:
                raise SystemExit("row %d uses %r, which has no colour" % (y, ch))
    return width, len(grid)


def runs(row):
    """Merge each horizontal run of one colour into a single rect. Fewer nodes,
    and no hairline seams between neighbouring rects at fractional zoom."""
    out = []
    x = 0
    while x < len(row):
        ch = row[x]
        if ch == ".":
            x += 1
            continue
        n = 1
        while x + n < len(row) and row[x + n] == ch:
            n += 1
        out.append((x, n, ch))
        x += n
    return out


def render(grid, ink, label, scale=4):
    w, h = check(grid, ink)
    rects = [
        '  <rect x="%d" y="%d" width="%d" height="1" fill="%s"/>' % (x, y, n, ink[ch])
        for y, row in enumerate(grid)
        for x, n, ch in runs(row)
    ]
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
        'width="%d" height="%d" shape-rendering="crispEdges" '
        'role="img" aria-label="%s">\n%s\n</svg>\n'
        % (w, h, w * scale, h * scale, label, "\n".join(rects)))


def lit(grid):
    return sum(1 for row in grid for ch in row if ch != ".")
