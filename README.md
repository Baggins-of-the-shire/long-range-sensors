# Long Range Sensors

Robotic telescope captures, logged like a console readout. Live at
<https://baggins-of-the-shire.github.io/long-range-sensors/>.

Images come from [Slooh](https://slooh.com) member missions. The SLOOH.COM
watermark in the corner of every frame is their attribution and stays put.

## The idea

Most amateur telescope frames are not good. They have gradients, satellite
trails, sensor banding, and planets forty pixels across. This site publishes
them anyway, with the fault named on the record, because a log that only shows
the wins is not a log. Two of the seven opening records are marked nominal.

## Editing

`photos.json` and `filters.json` are the only files you edit by hand.
Everything else derived from them is generated:

```
python3 build.py --check     # report, write nothing
python3 build.py             # write index.html and the filter block in style.css
python3 feed.py              # write feed.xml
```

Three more generators exist but only need rerunning if you change their source:

```
python3 icons.py             # icon.svg and the four PNGs, from one set of numbers
python3 probe.py             # probe.svg, the craft that crosses the console
python3 ship.py              # ship.svg, a second craft, not placed on the page
python3 qr.py                # qr.svg, and decodes it back to prove it scans
```

`probe.py` and `ship.py` share `pixel.py`, so a third craft is a grid and a
palette rather than another copy of the renderer.

`feed.py` is deterministic: `lastBuildDate` comes from the newest `published`
date, never the clock, so rerunning it on an unchanged gallery produces a
byte-identical file and no pointless commit.

`build.py` refuses to write at all if any of these is true:

- a record is missing any required field
- a record's `class` has no matching filter in `filters.json`
- two records share a slug
- an image named in `photos.json` is not in `images/`
- declared `w`/`h` do not match the actual file (checked wherever Pillow is installed)
- `grade` is not `nominal` or `degraded`
- a `degraded` record names no `fault`, or a `nominal` record carries one
- `photos.json` is not sorted newest `published` first
- a filter matches nothing
- alt text opens with "image of", "photo of" or "picture of"
- the home screen shortcut in `manifest.webmanifest` no longer points at the
  last record, which is what happens the moment a record is appended rather
  than prepended

The `?v=` on `style.css` and `app.js` is a content hash, so it changes exactly
when the file changes and never when it does not. That retires the stale
stylesheet problem rather than managing it.

## Adding a record

1. Harvest the frame from Slooh and prepare it: longest edge 1600, JPEG quality
   82, progressive, rebuilt into a fresh image so no metadata survives. Name it
   `YYYY-MM-DD-slug.jpg` from the **capture** date and drop it in `images/`.
2. Add an entry at the **top** of `photos.json`, with `published` set to today.
   Ordering on the page is by publish date, not capture date, so a frame from
   the archive lands at the top the day it goes up.
3. If it needs a class that does not exist, add it to `filters.json`
   (`key`, `label`, `code`, `colour`). Colour must be one of `tan`, `sky`,
   `periwinkle`, `peach`, `amber`.
4. `python3 build.py`, `python3 feed.py`, then commit and push.

If the shape of the gallery changes a lot, refresh `screenshot-narrow.jpg` and
`screenshot-wide.jpg`. They only feed the Android install card, and iOS ignores
them entirely, so this is not urgent.

## Publishing

Pushes happen **from the laptop only**. The cloud sandbox can read the remote
but its git proxy refuses the push.

The clone's credential is **pinned to a named account**, so whichever account
is active in the GitHub CLI no longer matters:

```
[credential "https://github.com"]
	helper =
	helper = "!f() { echo username=Baggins-of-the-shire; echo password=$(gh auth token --user joshtreu-pixel); }; f"
	username = Baggins-of-the-shire
```

Two things make that work. The empty first helper clears the inherited chain,
because Git Credential Manager is registered at the **system** level and would
otherwise answer first with the wrong account. `gh auth token --user` then
fetches a token for that account by name rather than whichever is active.
`joshtreu-pixel` is a stale label: it resolves to `Baggins-of-the-shire`, id
264735107. The account actually labelled `cyberbagginsoftheshire3791` is a
different one and gets a 403 here.

Verified by making the wrong account active and pushing anyway, which succeeds.

The clone also carries a repo-local identity so the global `user.email` never
reaches a commit.

After pushing, verify with a cache-busting query and give Pages more than fifty
seconds. A check that shows the old version usually means too soon rather than
a failed deploy.

## Design notes

Palette, type and chrome come from the Thoth kiosk LCARS theme so the two read
as one system: Antonio, true black, amber and peach on mauve, square corners
everywhere except the elbows.

- **Filtering is CSS.** Hidden checkboxes, `:has()` to hide all then restore
  each checked class. Separate rules mean the selection unions.
- **The viewer is `:target`.** It works with JavaScript blocked.
- **`app.js` is enhancement only**: live stardate, arrow-key and Escape
  navigation, neighbour preloading, scroll lock. Delete it and the site still
  works.
- The concave corner where the rail meets the content well is a single
  `radial-gradient`, not an image.
- **The icon is the console's own elbow** plus two bar segments, in mauve,
  amber and tan on black. `icons.py` holds one set of numbers and emits both
  the SVG and the PNGs from it, so the two renderers cannot drift apart. No
  stars and no telescope glyph: at 32 pixels in a browser tab anything finer
  turns to mush.
- **A survey probe crosses the strip above the plates**, drawn on a 30 by 16
  pixel grid by `probe.py`. It is not decoration for its own sake. Two of the
  opening records have a satellite drawn through them and one caption is about
  exactly that, so the thing drifting past is the thing that spoils the
  exposures. It parks rather than moves under
  `prefers-reduced-motion: reduce`.
- **There are two keep panels, not one.** `#keep-top` closes to `#top` and
  `#keep-below` closes to `#end`, because a single shared panel always returns
  one of its two entry points to the wrong end of the page. Same discipline as
  the sibling site: every `:target` panel puts you back where you came from.
- The probe is the top entry point, which makes it a moving target, so it
  pauses on hover and on keyboard focus. Watch out for anything else painting
  over it: the track hairline runs through the probe's exact centre and won
  the hit test until it was given `pointer-events: none`.
- **`qr.svg` encodes the site URL.** If the URL ever changes, rerun `qr.py`. A
  QR code pointing at the old address is worse than none, because it looks
  like it works.
