"""Draw the 23 November 2026 one-day news image.

Fresh code written for this entry. Layout follows the winning
cream-newspaper template: giant serif masthead, a UTC timeline strip,
a numbers strip, three large lead cards, ten small illustrated cards,
a world map with region counts, a numbered ALSO list, a DATE CHECK box
and a source/legend footer. All art is flat vector drawing in Pillow;
no photos, no network, no bundled fonts (system DejaVu only).
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 240, 220)
INK = (26, 26, 26)
RED = (179, 32, 44)
NAVY = (31, 46, 72)
GREEN = (30, 122, 52)
AMBER = (138, 109, 0)
GREY = (85, 85, 85)
BLUE = (31, 90, 160)
SEA = (223, 232, 230)
LAND = (203, 185, 138)
CARD = (255, 252, 244)

TAG_FILL = {
    "CONFIRMED": ((30, 122, 52), (223, 240, 226)),
    "OFFICIAL": ((138, 109, 0), (255, 243, 191)),
    "REPORTED": ((85, 85, 85), (232, 232, 232)),
    "FORECAST": ((31, 90, 160), (219, 233, 248)),
}

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill=INK, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def tag(draw, x, y, label):
    fg, bg = TAG_FILL[label]
    f = font(SANS_B, 9)
    w = draw.textlength(label, font=f) + 10
    draw.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=bg, outline=fg)
    draw.text((x + 5, y + 2), label, font=f, fill=fg)
    return w


def art(draw, kind, box):
    """Flat vector illustration inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    w, h = x1 - x0, y1 - y0
    if kind == "ship":
        draw.polygon([(x0 + 4, cy + 6), (x1 - 4, cy + 6), (x1 - 14, cy + 18),
                      (x0 + 14, cy + 18)], fill=NAVY)
        draw.rectangle([cx - 12, cy - 12, cx + 12, cy + 6], fill=RED)
        draw.line([(x0, y1 - 4), (x1, y1 - 4)], fill=BLUE, width=2)
        draw.line([(x0 + 8, y1 - 9), (x1 - 8, y1 - 9)], fill=BLUE, width=2)
        draw.ellipse([x1 - 26, y0 + 2, x1 - 10, y0 + 18], fill=(255, 170, 40))
    elif kind == "blast":
        for r, c in ((26, (255, 170, 40)), (18, RED), (10, (255, 220, 90))):
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
        draw.rectangle([x0 + 4, y1 - 14, x0 + 22, y1 - 2], fill=NAVY)
        draw.rectangle([x1 - 22, y1 - 10, x1 - 4, y1 - 2], fill=NAVY)
    elif kind == "globe":
        draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(120, 170, 200))
        draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=NAVY, width=2)
        draw.arc([cx - 24, cy - 24, cx + 24, cy + 24], 200, 340, fill=GREEN, width=6)
        draw.rectangle([cx + 16, cy - 26, cx + 22, cy + 10], fill=RED)
        draw.ellipse([cx + 12, cy + 6, cx + 26, cy + 20], fill=RED)
    elif kind == "chart":
        bars = [10, 18, 14, 26, 20, 30]
        bw = w // 7
        for i, b in enumerate(bars):
            bx = x0 + 4 + i * bw
            draw.rectangle([bx, y1 - 4 - b, bx + bw - 3, y1 - 4],
                           fill=RED if i == len(bars) - 1 else NAVY)
        draw.line([(x0 + 4, y0 + 8), (x1 - 4, y0 + 16)], fill=GREEN, width=2)
    elif kind == "capitol":
        draw.rectangle([x0 + 6, y1 - 8, x1 - 6, y1 - 2], fill=NAVY)
        draw.rectangle([x0 + 14, cy, x1 - 14, y1 - 8], fill=(240, 240, 240),
                       outline=NAVY)
        draw.pieslice([cx - 16, y0 + 2, cx + 16, y0 + 30], 180, 360, fill=RED)
        draw.rectangle([cx - 2, y0 - 2, cx + 2, y0 + 6], fill=INK)
    elif kind == "plane":
        draw.polygon([(x0 + 4, cy), (x1 - 16, cy - 8), (x1 - 4, cy),
                      (x1 - 16, cy + 8)], fill=NAVY)
        draw.polygon([(cx - 6, cy - 4), (cx + 2, cy - 16), (cx + 8, cy - 4)],
                     fill=NAVY)
        draw.line([(x0 + 2, y1 - 6), (x1 - 2, y1 - 6)], fill=GREY, width=2)
    elif kind == "flame":
        draw.polygon([(cx, y0 + 2), (cx + 14, cy + 6), (cx + 8, cy + 18),
                      (cx - 8, cy + 18), (cx - 14, cy + 6)], fill=(255, 140, 0))
        draw.polygon([(cx, cy - 2), (cx + 8, cy + 10), (cx - 8, cy + 10)],
                     fill=(255, 210, 60))
    elif kind == "building":
        draw.rectangle([x0 + 8, y0 + 8, x1 - 8, y1 - 2], fill=(230, 228, 220),
                       outline=NAVY, width=2)
        for i in range(3):
            for j in range(2):
                draw.rectangle([x0 + 14 + i * 14, y0 + 14 + j * 14,
                                x0 + 24 + i * 14, y0 + 24 + j * 14], fill=BLUE)
        draw.rectangle([cx - 8, y1 - 12, cx + 8, y1 - 2], fill=NAVY)
    elif kind == "shield":
        draw.polygon([(cx, y0 + 2), (cx + 20, y0 + 10), (cx + 20, cy + 6),
                      (cx, y1 - 2), (cx - 20, cy + 6), (cx - 20, y0 + 10)],
                     fill=NAVY)
        draw.text((cx, cy - 2), "24", font=font(SANS_B, 13), fill=(255, 255, 255),
                  anchor="mm")
    elif kind == "ball":
        draw.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(255, 255, 255),
                     outline=INK, width=2)
        draw.polygon([(cx, cy - 10), (cx + 10, cy - 3), (cx + 6, cy + 9),
                      (cx - 6, cy + 9), (cx - 10, cy - 3)], fill=INK)
        draw.line([(cx, cy - 22), (cx, cy - 10)], fill=INK, width=2)
    elif kind == "warning":
        draw.polygon([(cx, y0 + 2), (x1 - 4, y1 - 2), (x0 + 4, y1 - 2)],
                     fill=(255, 200, 40), outline=INK)
        draw.text((cx, cy + 2), "!", font=font(SANS_B, 20), fill=INK, anchor="mm")
    elif kind == "handshake":
        draw.ellipse([x0 + 6, cy - 12, cx + 2, cy + 12], outline=NAVY, width=3)
        draw.ellipse([cx - 2, cy - 12, x1 - 6, cy + 12], outline=RED, width=3)
    elif kind == "ban":
        draw.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=RED, width=4)
        draw.line([(cx - 16, cy + 16), (cx + 16, cy - 16)], fill=RED, width=4)
    else:
        draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=NAVY)


# Coarse continent outlines (lon, lat) for the schematic map.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 71), (-95, 69), (-80, 73), (-65, 62),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 29), (-125, 40), (-125, 49), (-150, 60), (-168, 66)],
    [(-80, 10), (-62, 9), (-52, 5), (-44, -3), (-35, -8), (-40, -20),
     (-48, -28), (-58, -35), (-65, -41), (-70, -52), (-73, -44), (-73, -30),
     (-77, -12), (-80, 1), (-80, 10)],
    [(-18, 35), (-10, 37), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 12), (48, 5), (42, -2), (40, -15), (33, -26), (26, -34),
     (19, -35), (15, -27), (12, -18), (9, -1), (-8, 4), (-17, 15), (-17, 28),
     (-18, 35)],
    [(-10, 37), (10, 38), (28, 36), (30, 36), (36, 36), (44, 39), (48, 42),
     (50, 47), (60, 46), (70, 55), (75, 60), (85, 68), (100, 73), (120, 73),
     (140, 72), (160, 70), (178, 66), (170, 60), (162, 56), (158, 52),
     (142, 45), (135, 35), (127, 33), (122, 31), (120, 23), (110, 20),
     (105, 9), (100, 6), (97, 16), (92, 21), (88, 22), (80, 15), (77, 8),
     (73, 20), (66, 25), (60, 25), (52, 26), (48, 29), (44, 29), (35, 28),
     (30, 36), (20, 40), (12, 44), (0, 40), (-9, 43), (-10, 37)],
    [(113, -22), (122, -14), (132, -12), (137, -15), (142, -11), (147, -19),
     (153, -27), (150, -37), (140, -38), (132, -32), (126, -32), (118, -35),
     (114, -30), (113, -22)],
    [(-45, 60), (-30, 60), (-22, 65), (-30, 70), (-45, 70), (-55, 64),
     (-45, 60)],
]


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 170) / 360.0 * (x1 - x0)
    y = y0 + (75 - lat) / 130.0 * (y1 - y0)
    return x, y


def draw_map(draw, data, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SEA)
    for poly in CONTINENTS:
        pts = [project(lon, lat, box) for lon, lat in poly]
        draw.polygon(pts, fill=LAND)
    draw.rectangle(box, outline=INK, width=2)
    offsets = {1: (26, -16), 2: (-8, -18), 5: (24, 10), 6: (-30, 12)}
    for pin in data["pins"]:
        px, py = project(pin["lon"], pin["lat"], box)
        ox, oy = offsets.get(pin["n"], (14, -14))
        bx, by = px + ox, py + oy
        draw.line([(px, py), (bx, by)], fill=INK, width=1)
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
        draw.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=RED, outline=(255, 255, 255))
        draw.text((bx, by), str(pin["n"]), font=font(SANS_B, 10),
                  fill=(255, 255, 255), anchor="mm")


def card(draw, box, item, num, big=False, lead=False):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=6, fill=CARD, outline=(200, 190, 165))
    pad = 10
    if lead:
        art_box = (x1 - 158, y0 + 34, x1 - 8, y1 - 46)
        tx = x0 + pad
        tw = art_box[0] - tx - 8
    elif big:
        art_box = (x1 - 100, y0 + 30, x1 - 8, y1 - 24)
        tx = x0 + pad
        tw = art_box[0] - tx - 8
    else:
        art_box = (x1 - 46, y0 + 6, x1 - 8, y0 + 32)
        tx = x0 + pad
        tw = x1 - x0 - 2 * pad
    art(draw, item["art"], art_box)
    # number badge + region (top-left; art sits top-right in small cards)
    draw.ellipse([x0 + pad, y0 + 6, x0 + pad + 18, y0 + 24], fill=RED)
    draw.text((x0 + pad + 9, y0 + 15), str(num), font=font(SANS_B, 11),
              fill=(255, 255, 255), anchor="mm")
    text(draw, (x0 + pad + 24, y0 + 8), item["region"].upper(),
         font(SANS_B, 9), fill=RED)
    if lead:
        hf = font(SANS_B, 17)
        lines = wrap(draw, item["headline"], hf, tw)[:2]
        hy = y0 + 30
        for ln in lines:
            text(draw, (tx, hy), ln, hf)
            hy += 21
        sf = font(SANS, 11)
        sl = wrap(draw, item["summary"], sf, tw)[:1]
        for ln in sl:
            text(draw, (tx, hy + 2), ln, sf)
            hy += 14
        if item.get("facts"):
            text(draw, (tx, y1 - 40), "  •  ".join(item["facts"]),
                 font(SANS_B, 9), fill=GREY)
        tag(draw, x0 + pad, y1 - 20, item["tag"])
        text(draw, (x1 - 8, y1 - 18), item["source"], font(SANS, 8), fill=GREY,
             anchor="ra")
        return
    if big:
        hf = font(SANS_B, 13)
        lines = wrap(draw, item["headline"], hf, tw)[:2]
        hy = y0 + 28
        for ln in lines:
            text(draw, (tx, hy), ln, hf)
            hy += 16
        sf = font(SANS, 11)
        sl = wrap(draw, item["summary"], sf, tw)[:2]
        for ln in sl:
            text(draw, (tx, hy + 2), ln, sf)
            hy += 13
        tag(draw, x0 + pad, y1 - 18, item["tag"])
        text(draw, (x1 - 8, y1 - 16), item["source"], font(SANS, 8), fill=GREY,
             anchor="ra")
        return
    # small card: headline below the top row, summary, tag at the bottom
    hf = font(SANS_B, 11)
    lines = wrap(draw, item["headline"], hf, tw)[:2]
    hy = y0 + 34
    for ln in lines:
        text(draw, (tx, hy), ln, hf)
        hy += 13
    sf = font(SANS, 9)
    sl = wrap(draw, item["summary"], sf, tw)[:2]
    sy = hy + 2
    for ln in sl:
        text(draw, (tx, sy), ln, sf)
        sy += 11
    tag(draw, x0 + pad, y1 - 18, item["tag"])
    text(draw, (x1 - 8, y1 - 16), item["source"], font(SANS, 7), fill=GREY,
         anchor="ra")


def build(data, out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 24
    x0, x1 = m, W - m
    y = 14
    # Masthead
    text(d, (W // 2, y), "THE WORLD IN ONE DAY", font(SANS_B, 13), fill=RED,
         anchor="ma")
    y += 20
    text(d, (W // 2, y), "MONDAY 23 NOVEMBER 2026", font(SERIF, 38),
         anchor="ma")
    y += 46
    stats = "38 STORIES  ·  7 REGIONS + MIDDLE EAST  ·  ALL FROM THIS MONDAY"
    text(d, (W // 2, y), stats, font(SANS_B, 11), anchor="ma")
    y += 20
    d.line([(x0, y), (x1, y)], fill=INK, width=2)
    y += 8
    # UTC strip
    d.rectangle([x0, y, x1, y + 46], fill=NAVY)
    text(d, (x0 + 8, y + 3), "THE DAY IN UTC", font(SANS_B, 10),
         fill=(255, 210, 60))
    cw = (x1 - x0) // 7
    for i, ev in enumerate(data["utc_strip"]):
        ex = x0 + i * cw + 6
        text(d, (ex, y + 15), ev["time"], font(SANS_B, 10), fill=(255, 210, 60))
        for j, ln in enumerate(wrap(d, ev["text"], font(SANS, 8), cw - 12)[:2]):
            text(d, (ex, y + 27 + j * 10), ln, font(SANS, 8),
                 fill=(255, 255, 255))
    y += 54
    # Numbers strip
    nw = (x1 - x0) // 6
    for i, num in enumerate(data["numbers"]):
        nx = x0 + i * nw
        if i:
            d.line([(nx, y + 4), (nx, y + 44)], fill=(200, 190, 165), width=1)
        text(d, (nx + nw // 2, y + 2), num["value"], font(SERIF, 24), fill=RED,
             anchor="ma")
        for j, ln in enumerate(wrap(d, num["label"], font(SANS, 8), nw - 10)[:2]):
            text(d, (nx + nw // 2, y + 28 + j * 10), ln, font(SANS, 8),
                 fill=GREY, anchor="ma")
    y += 48
    d.line([(x0, y), (x1, y)], fill=INK, width=1)
    y += 6
    # Lead card (full width)
    card(d, (x0, y, x1, y + 128), data["lead"], 1, lead=True)
    y += 136
    # Two big cards
    bw = (x1 - x0 - 8) // 2
    card(d, (x0, y, x0 + bw, y + 108), data["big"][0], 2, big=True)
    card(d, (x0 + bw + 8, y, x1, y + 108), data["big"][1], 3, big=True)
    y += 116
    # Ten small cards, two rows of five
    sw = (x1 - x0 - 4 * 8) // 5
    for row in range(2):
        for col in range(5):
            item = data["small"][row * 5 + col]
            sx = x0 + col * (sw + 8)
            card(d, (sx, y, sx + sw, y + 104), item, item["n"])
        y += 112
    # Map + region counts
    map_w = 640
    text(d, (x0, y), "WHERE IT HAPPENED", font(SANS_B, 11))
    draw_map(d, data, (x0, y + 16, x0 + map_w, y + 100))
    rx = x0 + map_w + 12
    text(d, (rx, y), "STORIES BY REGION", font(SANS_B, 11))
    ry = y + 18
    for reg in data["regions"]:
        text(d, (rx, ry), reg["name"], font(SANS_B, 10))
        text(d, (x1, ry), str(reg["count"]), font(SANS_B, 10), anchor="ra")
        ry += 12
    y += 108
    # ALSO list, three columns
    text(d, (x0, y), "ALSO ON MONDAY 23 NOVEMBER", font(SANS_B, 11))
    y += 16
    col_w = (x1 - x0 - 16) // 3
    for i, item in enumerate(data["also"]):
        col, row = divmod(i, 9)
        ax = x0 + col * (col_w + 8)
        ay = y + row * 12
        line = f"{item['n']}. {item['headline']}"
        while d.textlength(line, font=font(SANS, 10)) > col_w - 4 and len(line) > 20:
            line = line[:-5] + "…"
        text(d, (ax, ay), line, font(SANS, 10))
    y += 9 * 12 + 4
    # DATE CHECK box
    d.rounded_rectangle([x0, y, x1, y + 38], radius=4, outline=INK, width=1)
    text(d, (x0 + 8, y + 4), "DATE CHECK", font(SANS_B, 10), fill=RED)
    excl = "Left out (first reported before 23 Nov): " + "; ".join(
        data["date_check_excluded"][:4]) + "."
    for j, ln in enumerate(wrap(d, excl, font(SANS, 9), x1 - x0 - 16)[:2]):
        text(d, (x0 + 8, y + 17 + j * 11), ln, font(SANS, 9))
    y += 44
    # Footer
    d.line([(x0, y), (x1, y)], fill=INK, width=1)
    y += 5
    legend = ("CONFIRMED 2+ outlets  ·  OFFICIAL on the record  ·  "
              "REPORTED one outlet  ·  FORECAST")
    text(d, (x0, y), legend, font(SANS_B, 9))
    y += 13
    srcs = "Sources: " + ", ".join(data["sources"]) + ".  Original drawings."
    text(d, (x0, y), srcs, font(SANS, 9), fill=GREY)
    img.save(out_path, "PNG")
    return out_path


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "stories.json"), encoding="utf-8") as f:
        data = json.load(f)
    out = os.environ.get("OUTPUT_PATH") or os.path.join(base, "entry.png")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    build(data, out)
    print(out)
