# The World in One Day — 21 November 2026

A single 1024x1024 poster image that sums up the world's news of Saturday,
21 November 2026, built as an entry for the make.fun bounty
"news-image-20261121".

## The six stories

1. **Iran Conflict Threatens Bahrain Again** (Middle East)
   Reuters — "Bahrain warns residents of potential threat as Iran conflict persists"
2. **World Court: Myanmar Committed Genocide** (The Hague)
   Al Jazeera — "UN's top court finds Myanmar guilty of genocide against Rohingya"
3. **Trump, Xi, Putin Meet in Shenzhen** (Asia-Pacific)
   Reuters — "As Trump basks in summit pomp, China's Xi strengthens his hand"
4. **Russian Missiles Hit Kryvyi Rih** (Europe)
   Reuters — "Trump told European leaders they were spending a lot on Ukraine,
   Zelenskiy says" (reporting Russia's overnight attack on Kryvyi Rih, which
   killed at least two people, including a seven-year-old boy)
5. **AI Sell-Off Rocks Wall Street** (North America)
   Associated Press — "S&P 500 sinks 3.7% and Nasdaq composite goes negative
   for the year as tech sell-off worsens"
6. **COP31 Climate Talks Hit Deadlock** (Global)
   Al Jazeera — "Fossil fuel talks deadlock pushes COP31 climate summit into
   overtime"

## How it is built

- `panels/panel1.png` … `panel6.png` — six flat editorial illustrations, one
  per story, generated without any text in them.
- `build_image.py` — composes the panels into `entry.png` with Pillow:
  a dated front-page header ("SATURDAY, NOVEMBER 21, 2026 — THE WORLD IN ONE
  DAY"), a 2x3 grid, a region tag on each panel and a bold headline bar under
  each one. All lettering is rendered by PIL from Noto Sans Bold, so no text
  is baked into the generated artwork.
- `entry.png` — the final image: 1024x1024 PNG, 575,904 bytes.

## How the entry program works

`main.py` (Python standard library only) copies the `entry.png` stored beside
it into the output directory as `entry.png`. The output directory is read from
the `MAKEFUN_OUTPUT_DIR` environment variable and defaults to `/output`; the
directory is created if it does not exist yet. Running it any number of times
produces byte-identical output.
