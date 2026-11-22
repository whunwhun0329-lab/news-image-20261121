#!/usr/bin/env python3
"""Compose entry.png v2: a denser front-page style poster summing up the
world news of Saturday, 21 November 2026 in one 1024x1024 image.

Layout: dated header with story count, a 4-number stats strip, a 2x3 grid
of main stories (region tag, illustration, headline, one detail line,
source), a two-column "ALSO ON SATURDAY 21 NOVEMBER" list of short stories,
a DATE CHECK box listing famous stories deliberately left out for failing
the date rule, and a footer.

All text is rendered here with PIL from Noto Sans Bold; the generated panel
illustrations contain no text at all. Every story either happened on, or
was first reported on, Saturday 21 November 2026 (any time zone).
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"

W, H = 1024, 1024
BG = (246, 241, 231)        # warm paper
NAVY = (16, 36, 62)         # header / label bars
GOLD = (242, 177, 52)       # accents
WHITE = (255, 255, 255)
INK = (30, 34, 40)          # body text on paper
MUTE = (96, 100, 108)       # source lines / captions

MARGIN = 24
CONTENT_W = W - 2 * MARGIN  # 976

# (panel file, region tag, headline, detail line, source)
STORIES = [
    ("panel1.png", "MIDDLE EAST",
     "IRAN CONFLICT THREATENS BAHRAIN AGAIN",
     "Residents told to stay alert amid Iranian attacks",
     "REUTERS"),
    ("panel4.png", "EUROPE",
     "RUSSIAN MISSILES HIT KRYVYI RIH",
     "At least two killed, including a seven-year-old boy",
     "REUTERS"),
    ("panel6.png", "GLOBAL",
     "COP31 CLIMATE TALKS HIT DEADLOCK",
     "Draft text drops all mention of fossil fuels",
     "AL JAZEERA"),
    ("panel5.png", "NORTH AMERICA",
     "AI SELL-OFF ROCKS WALL STREET",
     "S&P 500 sinks 3.7%; Anthropic drops 9.1% post-IPO",
     "ASSOCIATED PRESS"),
    ("panel-mercury.png", "SPACE",
     "BEPICOLOMBO REACHES MERCURY AT LAST",
     "ESA-JAXA craft enters orbit; only the second ever",
     "ESA"),
    ("panel-vegas.png", "SPORT",
     "VERSTAPPEN WINS LAS VEGAS THRILLER",
     "35 lead changes; Norris beaten by just 0.639 seconds",
     "REUTERS"),
]

# (big number, caption line 1, caption line 2)
STATS = [
    ("-5.3%", "NASDAQ'S FRIDAY FALL", "IN THE AI SELL-OFF"),
    ("~200", "NATIONS DEADLOCKED", "AT COP31 TALKS"),
    ("0.639s", "VERSTAPPEN'S MARGIN", "IN LAS VEGAS"),
    ("8 YRS", "BEPICOLOMBO'S TRIP", "TO MERCURY"),
]

SHORTS_LEFT = [
    "GAZA \u2014 Israeli fire kills 4; 3 die in aid-truck strike",
    "WARSAW \u2014 Rutte vows to defend every inch of Poland",
    "SHENZHEN \u2014 Japan PM skips Taiwan envoy meeting at APEC",
    "RIYADH \u2014 Coalition downs 3 Houthi missiles over Riyadh",
    "KORDOFAN \u2014 Army says it took RSF's largest stronghold",
    "TURIN \u2014 Zverev beats Medvedev, into ATP Finals final",
    "MELBOURNE \u2014 Australia beat England by 3 wickets at MCG",
    "WELLINGTON \u2014 Rahul's 136 puts India 118 ahead of NZ",
]

SHORTS_RIGHT = [
    "LONDON \u2014 Leeds rout Chelsea 4-1; Arsenal draw 2-2",
    "ABUJA \u2014 CAF backs Infantino for FIFA re-election",
    "CARDIFF \u2014 Australia edge Wales 29-26 in rugby",
    "DOHA \u2014 Stirling KOs ex-champion Prochazka at UFC",
    "VATICAN \u2014 Pope Leo: music unites nations and faiths",
    "MALUKU \u2014 M6.8 quake off Indonesia; no tsunami threat",
    "BRAZIL \u2014 Storm leaves 4 dead, 162 hurt in the south",
]

DATE_CHECK_LINES = [
    "ICJ Myanmar genocide ruling \u2014 19 Nov \u00b7 Shenzhen three-leader summit \u2014 19 Nov \u00b7 Nvidia subpoena \u2014 19 Nov",
    "Russian missiles land in Poland \u2014 20 Nov \u00b7 Bayer $7.25bn Roundup settlement \u2014 20 Nov \u00b7 Indonesia\u2013Google \u2014 20 Nov",
]


def font(size):
    return ImageFont.truetype(FONT_BOLD, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def centered(draw, cx, y, s, f, fill):
    draw.text((cx - text_w(draw, s, f) / 2, y), s, font=f, fill=fill)


def crop_to_fill(img, tw, th, focal_y=0.42):
    """Resize/crop img to exactly tw x th, cropping around a focal height."""
    sw, sh = img.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - tw) // 2
    y = int((nh - th) * focal_y)
    y = max(0, min(nh - th, y))
    return img.crop((x, y, x + tw, y + th))


def fit_headline(draw, label, max_w):
    """Return (font, [lines]): one line if it fits at 24-20px, else two
    balanced lines at the largest size in 23-20px that fits."""
    for size in range(24, 19, -1):
        f = font(size)
        if text_w(draw, label, f) <= max_w:
            return f, [label]
    words = label.split()
    best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        for size in range(23, 19, -1):
            f = font(size)
            w = max(text_w(draw, a, f), text_w(draw, b, f))
            if w <= max_w:
                if best is None or size > best[0]:
                    best = (size, [a, b])
                break
    if best is None:  # last resort: 20px balanced split
        size = 20
        f = font(size)
        cand = None
        for i in range(1, len(words)):
            a, b = " ".join(words[:i]), " ".join(words[i:])
            w = max(text_w(draw, a, f), text_w(draw, b, f))
            if cand is None or w < cand[0]:
                cand = (w, [a, b])
        return f, cand[1]
    return font(best[0]), best[1]


def main():
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas, "RGBA")

    # ---- header band (0-118) ----
    draw.rectangle([0, 0, W, 118], fill=NAVY)
    draw.rectangle([0, 118, W, 123], fill=GOLD)
    centered(draw, W / 2, 12, "SATURDAY, NOVEMBER 21, 2026", font(40), WHITE)
    centered(draw, W / 2, 58, "T H E   W O R L D   I N   O N E   D A Y",
             font(25), GOLD)
    centered(draw, W / 2, 90,
             "21 STORIES \u00b7 EVERY ONE HAPPENED OR WAS FIRST REPORTED ON SAT 21 NOV 2026",
             font(15), WHITE)

    # ---- stats strip (129-201) ----
    col_w = CONTENT_W // 4
    num_f = font(36)
    cap_f = font(12)
    for i, (num, cap1, cap2) in enumerate(STATS):
        cx = MARGIN + col_w * i + col_w / 2
        centered(draw, cx, 131, num, num_f, NAVY)
        centered(draw, cx, 173, cap1, cap_f, MUTE)
        centered(draw, cx, 187, cap2, cap_f, MUTE)
        if i:
            x = MARGIN + col_w * i
            draw.line([x, 137, x, 195], fill=(200, 192, 175), width=2)
    draw.line([MARGIN, 203, W - MARGIN, 203], fill=(200, 192, 175), width=2)

    # ---- main grid (209-727): 2 cols x 3 rows, cell 483x166 ----
    grid_top = 209
    gap = 10
    cell_w = (CONTENT_W - gap) // 2
    cell_h = 166
    img_h = 74
    bar_h = cell_h - img_h  # 92
    tag_f = font(17)
    det_f = font(14)
    src_f = font(11)
    for idx, (fname, region, headline, detail, source) in enumerate(STORIES):
        r, c = divmod(idx, 2)
        x0 = MARGIN + c * (cell_w + gap)
        y0 = grid_top + r * (cell_h + gap)

        panel = Image.open(os.path.join(HERE, "panels", fname)).convert("RGB")
        tile = crop_to_fill(panel, cell_w, img_h)
        canvas.paste(tile, (x0, y0))

        tw = text_w(draw, region, tag_f)
        pill = [x0 + 8, y0 + 8, x0 + 8 + tw + 20, y0 + 8 + 17 + 10]
        draw.rounded_rectangle(pill, radius=7, fill=(10, 20, 35, 215))
        draw.text((x0 + 18, y0 + 13), region, font=tag_f, fill=GOLD)

        bar_y = y0 + img_h
        draw.rectangle([x0, bar_y, x0 + cell_w, y0 + cell_h], fill=NAVY)
        hf, lines = fit_headline(draw, headline, cell_w - 24)
        head_h = (hf.size + 5) * len(lines) - 5
        det_h, src_h = 17, 13
        total = head_h + 3 + det_h + 2 + src_h
        ty = bar_y + (bar_h - total) // 2
        for line in lines:
            draw.text((x0 + 12, ty), line, font=hf, fill=WHITE)
            ty += hf.size + 5
        ty += 3 - 5
        draw.text((x0 + 12, ty), detail, font=det_f, fill=(214, 222, 235))
        ty += det_h + 2
        draw.text((x0 + 12, ty), "SOURCE: " + source, font=src_f, fill=GOLD)

    # ---- ALSO section ----
    also_y = 737
    draw.text((MARGIN, also_y), "ALSO ON SATURDAY 21 NOVEMBER", font=font(19),
              fill=NAVY)
    draw.rectangle([MARGIN, also_y + 25, W - MARGIN, also_y + 28], fill=GOLD)

    short_f = font(14)
    col_gap = 16
    scol_w = (CONTENT_W - col_gap) // 2
    row_h = 19
    shorts_top = 773
    numbered = list(enumerate(
        SHORTS_LEFT + SHORTS_RIGHT, start=1))
    left = numbered[:len(SHORTS_LEFT)]
    right = numbered[len(SHORTS_LEFT):]
    for col_items, x0 in ((left, MARGIN), (right, MARGIN + scol_w + col_gap)):
        for j, (n, s) in enumerate(col_items):
            line = "%d. %s" % (n, s)
            f = short_f
            if text_w(draw, line, f) > scol_w:
                f = font(13)  # safety fallback; lines are sized to fit at 14
            draw.text((x0, shorts_top + j * row_h), line, font=f, fill=INK)

    # ---- DATE CHECK box (929-989) ----
    box = [MARGIN, 929, W - MARGIN, 989]
    draw.rounded_rectangle(box, radius=8, outline=NAVY, width=2)
    draw.text((MARGIN + 12, 936), "DATE CHECK \u2014 LEFT OUT AS NOT 21 NOVEMBER NEWS:",
              font=font(13), fill=NAVY)
    item_f = font(12)
    draw.text((MARGIN + 12, 955), DATE_CHECK_LINES[0], font=item_f, fill=INK)
    draw.text((MARGIN + 12, 971), DATE_CHECK_LINES[1], font=item_f, fill=INK)

    # ---- footer ----
    centered(draw, W / 2, 997,
             "Every story happened, or was first reported, on Saturday 21 November 2026. Sources named with each story.",
             font(12), MUTE)

    out = os.path.join(HERE, "entry.png")
    canvas.save(out, optimize=True)
    size = os.path.getsize(out)
    if size > 1048576:  # palette-quantize the flat artwork until it fits
        for colors in (256, 192, 128):
            q = canvas.quantize(colors=colors, method=Image.MEDIANCUT)
            q.save(out, optimize=True)
            size = os.path.getsize(out)
            if size <= 1048576:
                break
    print("entry.png:", canvas.size, size, "bytes")


if __name__ == "__main__":
    main()
