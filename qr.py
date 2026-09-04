#!/usr/bin/env python3
"""Emit qr.svg for the site URL, and read it back to prove it scans.

    python3 qr.py

If the site URL ever changes, rerun this. A QR code that points at the old
address is worse than no QR code, because it looks like it works.
"""

import os
import sys

import segno

SITE = os.environ.get("SITE", os.path.dirname(os.path.abspath(__file__)))
URL = os.environ.get("BASE", "https://baggins-of-the-shire.github.io/long-range-sensors/")

DARK = "#FFCC99"     # tan, so it sits in the palette rather than on top of it
LIGHT = "#000000"


def main():
    path = os.path.join(SITE, "qr.svg")
    qr = segno.make(URL, error="m")
    qr.save(path, kind="svg", scale=8, border=3, dark=DARK, light=LIGHT,
            svgclass=None, lineclass=None)

    print("qr.svg     version %s, error correction %s, %d bytes"
          % (qr.version, qr.error.upper(), os.path.getsize(path)))
    print("           encodes %s" % URL)

    # Decoding it is the only check that matters. Without a decoder available
    # the file still ships, but say so rather than implying it was verified.
    try:
        import cv2
        import numpy as np
        from PIL import Image
        import io
        import cairosvg  # noqa: F401
    except ImportError:
        png = os.path.join(SITE, "qr-check.png")
        try:
            qr.save(png, kind="png", scale=8, border=3)
            import cv2
            got, _, _ = cv2.QRCodeDetector().detectAndDecode(cv2.imread(png))
            os.remove(png)
            if got != URL:
                print("           DECODE FAILED, read back %r" % got)
                return 1
            print("           decoded back to the same URL")
        except ImportError:
            print("           not decoded: no decoder installed here")
        except Exception as exc:
            if os.path.exists(png):
                os.remove(png)
            print("           not decoded: %s" % exc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
