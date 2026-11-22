#!/usr/bin/env python3
"""Compose entry.png: a front-page style poster summing up the world news
of Saturday, 21 November 2026 in one 1024x1024 image.

All text is rendered here with PIL from a TrueType font; the generated
panel illustrations contain no text at all.
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

HEADER_H = 148
MARGIN = 24
GAP = 14
GRID_TOP = HEADER_H + 16
GRID_BOTTOM = H - 16

STORIES = [
    ("panel1.png", "MIDDLE EAST",    "IRAN CONFLICT THREATENS BAHRAIN AGAIN"),
    ("panel2.png", "THE HAGUE",      "WORLD COURT: MYANMAR COMMITTED GENOCIDE"),
    ("panel3.png", "ASIA-PACIFIC",   "TRUMP, XI, PUTIN MEET IN SHENZHEN"),
    ("panel4.png", "EUROPE",         "RUSSIAN MISSILES HIT KRYVYI RIH"),
    ("panel5.png", "NORTH AMERICA",  "AI SELL-OFF ROCKS WALL STREET"),
    ("panel6.png", "GLOBAL",         "COP31 CLIMATE TALKS HIT DEADLOCK"),
]

BAR_H = 84  # label bar height inside each cell


def font(size):
    return ImageFont.truetype(FONT_BOLD, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


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


def fit_label(draw, label, max_w):
    """Return (font, [lines]) with lines at >= 28px that fit max_w."""
    for size in range(34, 27, -1):
        f = font(size)
        if text_w(draw, label, f) <= max_w:
            return f, [label]
    # two balanced lines at 30px, shrinking to 28px if needed
    words = label.split()
    best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        f = font(30)
        w = max(text_w(draw, a, f), text_w(draw, b, f))
        if best is None or w < best[0]:
            best = (w, [a, b])
    size = 30
    while size > 28 and best[0] > max_w:
        size -= 1
        f = font(size)
        best = (max(text_w(draw, best[1][0], f), text_w(draw, best[1][1], f)), best[1])
    return font(size), best[1]


def main():
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas, "RGBA")

    # ---- header band ----
    draw.rectangle([0, 0, W, HEADER_H], fill=NAVY)
    draw.rectangle([0, HEADER_H, W, HEADER_H + 5], fill=GOLD)
    date_f = font(54)
    date = "SATURDAY, NOVEMBER 21, 2026"
    dw = text_w(draw, date, date_f)
    draw.text(((W - dw) / 2, 24), date, font=date_f, fill=WHITE)
    sub_f = font(27)
    sub = "T H E   W O R L D   I N   O N E   D A Y"
    sw = text_w(draw, sub, sub_f)
    draw.text(((W - sw) / 2, 96), sub, font=sub_f, fill=GOLD)

    # ---- grid ----
    cols, rows = 2, 3
    cell_w = (W - 2 * MARGIN - (cols - 1) * GAP) // cols
    cell_h = (GRID_BOTTOM - GRID_TOP - (rows - 1) * GAP) // rows
    img_h = cell_h - BAR_H

    tag_f = font(21)
    for idx, (fname, region, label) in enumerate(STORIES):
        r, c = divmod(idx, cols)
        x0 = MARGIN + c * (cell_w + GAP)
        y0 = GRID_TOP + r * (cell_h + GAP)

        panel = Image.open(os.path.join(HERE, "panels", fname)).convert("RGB")
        tile = crop_to_fill(panel, cell_w, img_h)
        canvas.paste(tile, (x0, y0))

        # region tag pill over the image, top-left
        tw = text_w(draw, region, tag_f)
        pad_x, pad_y = 11, 6
        pill = [x0 + 10, y0 + 10, x0 + 10 + tw + 2 * pad_x, y0 + 10 + 21 + 2 * pad_y + 4]
        draw.rounded_rectangle(pill, radius=8, fill=(10, 20, 35, 215))
        draw.text((x0 + 10 + pad_x, y0 + 10 + pad_y), region, font=tag_f, fill=GOLD)

        # label bar
        bar_y = y0 + img_h
        draw.rectangle([x0, bar_y, x0 + cell_w, y0 + cell_h], fill=NAVY)
        lf, lines = fit_label(draw, label, cell_w - 28)
        line_h = lf.size + 8
        total_h = line_h * len(lines) - 8
        ty = bar_y + (BAR_H - total_h) // 2
        for line in lines:
            draw.text((x0 + 14, ty), line, font=lf, fill=WHITE)
            ty += line_h

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
