#!/usr/bin/env python3
"""Render the news-image-20261124 entry: a one-page newspaper front page
summing up Tuesday 24 November 2026 in six verified stories.

Drawn entirely with Pillow primitives (no photos, no copied artwork).
Deterministic: fixed layout, fixed fonts, no timestamps, no randomness,
so repeated runs produce byte-identical PNG output.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (22, 35, 58)
RED = (180, 35, 24)
TEAL = (18, 92, 96)
GREY = (90, 92, 96)
CARD = (255, 255, 255)
LINE = (180, 176, 164)
GOLD = (176, 132, 32)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, fill, max_w, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def badge(draw, cx, cy, r, label, bg=RED, fg=(255, 255, 255)):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=bg)
    f = font(SANS_B, 20)
    tw = draw.textlength(label, font=f)
    draw.text((cx - tw / 2, cy - 13), label, font=f, fill=fg)


def icon_ship(draw, x, y, s, color):
    # Simple warship silhouette: hull, bow, mast, waves.
    draw.polygon([(x, y + 22 * s), (x + 78 * s, y + 22 * s),
                  (x + 66 * s, y + 38 * s), (x + 10 * s, y + 38 * s)],
                 fill=color)
    draw.polygon([(x + 78 * s, y + 22 * s), (x + 92 * s, y + 28 * s),
                  (x + 78 * s, y + 32 * s)], fill=color)
    draw.rectangle([x + 30 * s, y + 4 * s, x + 36 * s, y + 22 * s], fill=color)
    draw.rectangle([x + 20 * s, y + 10 * s, x + 52 * s, y + 16 * s], fill=color)
    for i, wx in enumerate((0, 26, 52, 78)):
        draw.arc([x + wx * s, y + 44 * s, x + (wx + 22) * s, y + 56 * s],
                 start=180, end=360, fill=color, width=max(2, int(3 * s)))


def icon_quake(draw, x, y, s, color):
    # Mountain ridge with a seismic zigzag above it.
    draw.polygon([(x, y + 46 * s), (x + 26 * s, y + 8 * s),
                  (x + 44 * s, y + 30 * s), (x + 58 * s, y + 12 * s),
                  (x + 92 * s, y + 46 * s)], fill=color)
    pts = [(x, y + 4 * s), (x + 12 * s, y + 4 * s), (x + 18 * s, y - 8 * s),
           (x + 26 * s, y + 10 * s), (x + 34 * s, y - 4 * s),
           (x + 44 * s, y + 8 * s), (x + 56 * s, y - 6 * s),
           (x + 66 * s, y + 6 * s), (x + 78 * s, y - 2 * s),
           (x + 92 * s, y + 4 * s)]
    draw.line(pts, fill=RED, width=max(2, int(3 * s)), joint="curve")


def icon_shield(draw, x, y, s, color):
    # Shield outline with a diagonal delay bar.
    draw.polygon([(x + 46 * s, y), (x + 88 * s, y + 12 * s),
                  (x + 88 * s, y + 44 * s), (x + 46 * s, y + 72 * s),
                  (x + 4 * s, y + 44 * s), (x + 4 * s, y + 12 * s)],
                 outline=color, width=max(3, int(4 * s)))
    draw.line([(x + 16 * s, y + 56 * s), (x + 76 * s, y + 16 * s)],
              fill=RED, width=max(3, int(5 * s)))


def icon_satellite(draw, x, y, s, color):
    # Satellite body with solar panels on an orbit ellipse.
    draw.ellipse([x - 6 * s, y - 14 * s, x + 98 * s, y + 58 * s],
                 outline=color, width=max(2, int(3 * s)))
    draw.rectangle([x + 38 * s, y + 14 * s, x + 56 * s, y + 34 * s],
                   fill=color)
    draw.rectangle([x + 4 * s, y + 18 * s, x + 36 * s, y + 30 * s],
                   fill=color)
    draw.rectangle([x + 58 * s, y + 18 * s, x + 90 * s, y + 30 * s],
                   fill=color)
    draw.line([(x + 40 * s, y + 34 * s), (x + 30 * s, y + 48 * s)],
              fill=color, width=max(2, int(3 * s)))
    draw.ellipse([x + 62 * s, y + 2 * s, x + 72 * s, y + 12 * s],
                 fill=RED)


def icon_chat(draw, x, y, s, color):
    # Speech bubble with an exclamation mark.
    draw.rounded_rectangle([x, y, x + 84 * s, y + 56 * s],
                           radius=int(12 * s), fill=color)
    draw.polygon([(x + 16 * s, y + 56 * s), (x + 30 * s, y + 56 * s),
                  (x + 18 * s, y + 72 * s)], fill=color)
    draw.rectangle([x + 38 * s, y + 12 * s, x + 46 * s, y + 34 * s],
                   fill=(255, 255, 255))
    draw.ellipse([x + 38 * s, y + 40 * s, x + 46 * s, y + 48 * s],
                 fill=(255, 255, 255))


def card(draw, x, y, w, h, num, kicker, headline, body, source, icon):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=CARD, outline=LINE, width=2)
    badge(draw, x + 30, y + 32, 17, str(num))
    f_kick = font(SANS_B, 15)
    draw.text((x + 56, y + 22), kicker.upper(), font=f_kick, fill=RED)
    icon(draw, x + w - 108, y + 18, 0.85, TEAL)
    f_head = font(SERIF_B, 24)
    top = y
    y = draw_wrapped(draw, (x + 22, y + 58), headline, f_head, INK,
                     w - 44, 29)
    f_body = font(SANS, 15)
    y = draw_wrapped(draw, (x + 22, y + 8), body, f_body, (52, 56, 64),
                     w - 44, 19) + 6
    f_src = font(SANS_B, 12)
    draw.text((x + 22, top + h - 26), source, font=f_src, fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.text((36, 26), "THE WORLD IN ONE IMAGE", font=font(SERIF_B, 52),
           fill=INK)
    d.line([(36, 96), (988, 96)], fill=RED, width=4)
    d.text((36, 108), "TUESDAY 24 NOVEMBER 2026",
           font=font(SANS_B, 24), fill=RED)
    d.text((36, 140), "Six stories that defined the day  ·  Reported 24 November 2026",
           font=font(SANS, 17), fill=GREY)

    # ---- Lead story panel ----
    lx, ly, lw, lh = 36, 172, 952, 256
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=12, fill=INK)
    badge(d, lx + 32, ly + 34, 18, "1")
    d.text((lx + 58, ly + 22), "LEAD  ·  EUROPE / NATO", font=font(SANS_B, 16),
           fill=(255, 214, 64))
    f_lead = font(SERIF_B, 37)
    y = draw_wrapped(d, (lx + 24, ly + 56),
                     "MOSCOW WARNS ESTONIA OF \u2018OPEN WAR\u2019",
                     f_lead, (255, 255, 255), 620, 45)
    f_lbody = font(SANS, 17)
    draw_wrapped(d, (lx + 24, y + 8),
                 "Russia summons Estonia\u2019s envoy over Tallinn\u2019s plan to shut "
                 "its border crossings from 1 December, calling it \u201con the verge "
                 "of triggering open war\u201d. Estonia denies the airspace claim.",
                 f_lbody, (214, 220, 232), 620, 23)
    # Drawn art: border fence posts under a red warning triangle.
    ax, ay = 720, 196
    d.polygon([(ax + 110, ay), (ax + 190, ay + 130), (ax + 30, ay + 130)],
              fill=RED)
    d.text((ax + 98, ay + 52), "!", font=font(SANS_B, 56), fill=(255, 255, 255))
    for i in range(4):
        px = ax + i * 52
        d.rectangle([px - 3, ay + 146, px + 3, ay + 192], fill=(255, 214, 64))
    d.rectangle([ax - 3, ay + 146, ax + 159, ay + 152], fill=(255, 214, 64))
    d.rectangle([ax - 3, ay + 170, ax + 159, ay + 176], fill=(255, 214, 64))
    d.text((lx + 24, ly + lh - 30), "Source: Reuters, 24 Nov 2026",
           font=font(SANS_B, 12), fill=(150, 160, 178))

    # ---- Story cards ----
    stories = [
        dict(num=2, kicker="War at sea · Libya",
             headline="Ukraine says its drones sank a Russian warship off Libya",
             body="Kyiv says naval drones sank the corvette Merkury at Benghazi "
                  "and hit the cargo ship Angara.",
             source="Source: Middle East Eye / NPR, 24 Nov 2026",
             icon=icon_ship),
        dict(num=3, kicker="Disaster · Asia",
             headline="5.6-magnitude quake shakes Nepal\u2019s border with China",
             body="The tremor strikes Taplejung at 7:17 a.m.; shaking is felt "
                  "across Nepal, India, Bhutan and Bangladesh.",
             source="Source: Nepal NEMRC / EMSC, 24 Nov 2026",
             icon=icon_quake),
        dict(num=4, kicker="Defence · Ukraine",
             headline="US delays Patriot missiles promised to Ukraine",
             body="About 60 interceptors already agreed are still awaiting "
                  "approval, the Financial Times reports.",
             source="Source: Financial Times, 24 Nov 2026",
             icon=icon_shield),
        dict(num=5, kicker="Space · Europe",
             headline="Germany heeds nuclear-satellite warning",
             body="Berlin is acting on reports Russia may launch a nuclear-armed "
                  "satellite, Sputnik-S, later this year.",
             source="Source: BND / The Independent, 24 Nov 2026",
             icon=icon_satellite),
    ]
    cw, ch, gap = 468, 198, 16
    positions = [(36, 440), (520, 440), (36, 650), (520, 650)]
    for story, (x, y) in zip(stories, positions):
        card(d, x, y, cw, ch, **story)

    # ---- Bottom full-width story ----
    bx, by, bw, bh = 36, 860, 952, 108
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10,
                        fill=CARD, outline=LINE, width=2)
    badge(d, bx + 30, by + 32, 17, "6")
    d.text((bx + 56, by + 22), "TECH & LAW  ·  UNITED STATES",
           font=font(SANS_B, 15), fill=RED)
    icon_chat(d, bx + bw - 118, by + 20, 0.85, TEAL)
    d.text((bx + 22, by + 56),
           "Two US states sue SpaceX over Grok sexual images",
           font=font(SERIF_B, 24), fill=INK)
    d.text((bx + 22, by + 86),
           "Virginia and Oregon file the first state lawsuits over Grok, alleging "
           "non-consensual sexual images, including of children.",
           font=font(SANS, 15), fill=(52, 56, 64))

    # ---- Footer ----
    d.line([(36, 982), (988, 982)], fill=LINE, width=2)
    d.text((36, 992),
           "Sources: Reuters · Financial Times · The Independent · Middle East Eye · "
           "Nepal NEMRC · AP  —  All stories reported on Tuesday 24 November 2026.",
           font=font(SANS, 13), fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
