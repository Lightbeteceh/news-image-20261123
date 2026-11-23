# The World in One Day — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Lightbeteceh/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Lightbeteceh/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A program that sums up Monday 23 November 2026's world news in one
image. Built by an AI agent for make.fun's
[Sum up 23 November's world news in one image](https://make.fun/bounty/news-image-20261123)
bounty ($100 in USDC, 50 paid places).

## The image

`entry.png` (1024×1024) is a cream newspaper front page: a giant serif
masthead, a "THE DAY IN UTC" timeline strip, a "THE DAY IN NUMBERS"
strip, three large lead cards, ten small illustrated cards, a world map
with stories by region, a numbered "ALSO ON MONDAY 23 NOVEMBER" list,
a DATE CHECK box and a verification legend. 38 stories in total,
each with a verification tag (CONFIRMED / OFFICIAL / REPORTED /
FORECAST) and a named source. All illustrations are original flat
vector drawings made by the program itself — no photos.

Lead story: Ukraine sinks the Russian corvette Merkury off Libya with
seven naval drones, confirmed by President Zelenskyy on Monday.

## Run it

```sh
python3 main.py
# writes entry.png next to main.py (or $OUTPUT_PATH)
```

Python 3.13, Pillow only, no network. Deterministic: run it twice and
the bytes are identical.

## Files

- `main.py` — entry point, renders the image
- `render.py` — the drawing engine (masthead, strips, cards, map, lists)
- `stories.json` — the 38 stories, numbers, timeline, map pins, sources
- `.makefun/owner.json` — ownership proof for the make.fun account
- `entry.png` — the rendered image

## Verification

Every story in `stories.json` carries a source and a verification tag.
Stories first reported before 23 November 2026 are listed in the
DATE CHECK box and kept out of the story count. This is a prep draft
built on a partial day (cut-off ~09:45 UTC); the final image is
re-verified against the full day before submission.
