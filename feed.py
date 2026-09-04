#!/usr/bin/env python3
"""Write feed.xml from photos.json, deterministically.

RSS 2.0, one item per record, in photos.json order, which is newest
published first. Nothing in the output depends on the moment the script
runs, so a rerun over unchanged data produces a byte-identical file and
no pointless commit reaches the repo.

    python3 feed.py             write feed.xml

photos.json is validated by build.py, not here. SITE env var overrides the
directory and BASE the public URL, which is how the tests drive it.
"""

import html
import json
import os
import sys
from datetime import datetime, timezone
from email.utils import format_datetime

SITE = os.environ.get("SITE", os.path.dirname(os.path.abspath(__file__)))
BASE = os.environ.get("BASE",
                      "https://baggins-of-the-shire.github.io/long-range-sensors/")

TITLE = "Long Range Sensors"
DESCRIPTION = ("Robotic telescope captures, logged with the fault written on "
               "the label.")


def load(name):
    with open(os.path.join(SITE, name), encoding="utf-8") as fh:
        return json.load(fh)


def e(text):
    return html.escape(str(text), quote=True)


def cdata(text):
    """Wrap markup in CDATA, splitting any ]]> so it cannot close early."""
    return "<![CDATA[%s]]>" % text.replace("]]>", "]]]]><![CDATA[>")


def rfc822(day):
    """2026-09-04 -> Fri, 04 Sep 2026 12:00:00 +0000

    Noon UTC keeps a record on its intended date in every reader timezone.
    format_datetime carries its own English weekday and month tables, so the
    stamp does not move with the locale the way strftime would.
    """
    when = datetime.strptime(day, "%Y-%m-%d").replace(hour=12, tzinfo=timezone.utc)
    return format_datetime(when)


def image_url(p):
    return BASE + "images/" + p["file"]


def image_bytes(p):
    """Readers trust enclosure length, so it comes from the file, not the JSON."""
    return os.path.getsize(os.path.join(SITE, "images", p["file"]))


def describe(p):
    """The body of one item: the picture, the note, then the label line."""
    label = "%s, %s filter." % (p["instrument"], p["filter"])
    if p["grade"] == "degraded":
        label += " Degraded: %s." % p["fault"]
    return ('<p><img src="{img}" alt="{alt}" width="{w}" height="{h}"></p>\n'
            '<p>{note}</p>\n'
            '<p>{label}</p>').format(img=e(image_url(p)), alt=e(p["alt"]),
                                     w=p["w"], h=p["h"], note=e(p["note"]),
                                     label=e(label))


def render_item(p):
    link = BASE + "#p-" + p["slug"]
    return """    <item>
      <title>{title}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <pubDate>{pubdate}</pubDate>
      <category>{cls}</category>
      <description>{body}</description>
      <enclosure url="{img}" length="{length}" type="image/jpeg"/>
    </item>
""".format(title=e(p["name"]), link=e(link), pubdate=e(rfc822(p["published"])),
           cls=e(p["class"]), body=cdata(describe(p)), img=e(image_url(p)),
           length=image_bytes(p))


def render(photos):
    # Items keep photos.json order, which is publish date descending. The
    # build stamp is the newest publish date, never the clock, because a
    # clock in the output means every rerun is a diff.
    newest = max(p["published"] for p in photos)
    items = "".join(render_item(p) for p in photos)

    return """<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{title}</title>
    <link>{base}</link>
    <description>{description}</description>
    <language>en</language>
    <lastBuildDate>{built}</lastBuildDate>
    <atom:link rel="self" href="{base}feed.xml" type="application/rss+xml"/>
{items}  </channel>
</rss>
""".format(title=e(TITLE), base=e(BASE), description=e(DESCRIPTION),
           built=e(rfc822(newest)), items=items)


def main():
    photos = load("photos.json")
    if not photos:
        print("photos.json is empty, refusing to write an empty feed")
        return 1

    feed = render(photos)
    path = os.path.join(SITE, "feed.xml")

    old = ""
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            old = fh.read()

    changed = feed != old
    if changed:
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(feed)

    print("feed.xml %s: %d items, newest %s, %d bytes"
          % ("written" if changed else "unchanged", len(photos),
             max(p["published"] for p in photos), len(feed.encode("utf-8"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
