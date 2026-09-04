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
```

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
4. `python3 build.py`, then commit and push.

## Publishing

Pushes happen **from the laptop only**. The cloud sandbox can read the remote
but its git proxy refuses the push.

```
gh auth switch --user joshtreu-pixel     # stale label; this IS Baggins-of-the-shire
git -C <clone> push origin main
```

The account labelled `cyberbagginsoftheshire3791` in the GitHub CLI is a
different account and gets a 403 on this repo. The clone carries a repo-local
identity so the global `user.email` never reaches a commit.

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
