#!/usr/bin/env python3
"""Generate entry.png: a newspaper-style front page summing up the world news
of Tuesday 24 November 2026, drawn entirely in code with Pillow.

Deterministic: fixed text, fixed fonts, no randomness, no timestamps.
Run:  python3 generate.py            -> writes entry.png (1024x1024)
       python3 generate.py --output out.png
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)   # newsprint off-white
INK = (20, 20, 20)
GREY = (90, 90, 90)
RED = (158, 27, 27)      # masthead accent
RULE = (40, 40, 40)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"

MARGIN = 36
CW = W - 2 * MARGIN  # content width


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width. Returns list of lines."""
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


def draw_wrapped(draw, text, fnt, x, y, max_w, leading, fill=INK):
    """Draw wrapped text; return y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, text, x, y, size=15):
    fnt = font(SANS_B, size)
    draw.text((x, y), text.upper(), font=fnt, fill=RED)
    return y + size + 6


def headline(draw, text, fnt, x, y, max_w, leading):
    return draw_wrapped(draw, text, fnt, x, y, max_w, leading)


def body(draw, text, x, y, max_w, size=17, leading=23):
    return draw_wrapped(draw, text, font(SERIF, size), x, y, max_w, leading)


def rule(draw, x, y, w, width=2):
    draw.line([(x, y), (x + w, y)], fill=RULE, width=width)
    return y + width + 2


def skyline(draw, x, y, w, h):
    """Simple code-drawn city skyline silhouette for the lead story art."""
    draw.rectangle([x, y, x + w, y + h], fill=(233, 226, 210))
    # buildings, left to right
    buildings = [
        (0.00, 0.45, 0.10, 1.00),
        (0.11, 0.30, 0.08, 1.00),
        (0.20, 0.55, 0.09, 1.00),
        (0.30, 0.18, 0.07, 1.00),   # tall tower (PIF Tower)
        (0.38, 0.50, 0.10, 1.00),
        (0.49, 0.35, 0.08, 1.00),
        (0.58, 0.60, 0.09, 1.00),
        (0.68, 0.28, 0.08, 1.00),
        (0.77, 0.48, 0.09, 1.00),
        (0.87, 0.38, 0.13, 1.00),
    ]
    for fx, fy, fw, fh in buildings:
        bx = x + int(fx * w)
        bw = int(fw * w)
        by = y + int(fy * h)
        draw.rectangle([bx, by, bx + bw, y + h], fill=(70, 70, 70))
    # the tall tower gets a pointed top and a small flash above it
    tx = x + int(0.30 * w)
    tw = int(0.07 * w)
    draw.polygon([(tx, y + int(0.18 * h)), (tx + tw // 2, y + int(0.06 * h)),
                  (tx + tw, y + int(0.18 * h))], fill=(70, 70, 70))
    cx, cy = tx + tw // 2, y + int(0.02 * h)
    for dx, dy in [(0, -14), (0, 14), (-14, 0), (14, 0), (-10, -10), (10, -10),
                   (-10, 10), (10, 10)]:
        draw.line([(cx, cy), (cx + dx, cy + dy)], fill=RED, width=3)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    # caption
    draw.text((x, y + h + 4), "Riyadh's financial district. Illustration drawn in code.",
              font=font(SANS, 11), fill=GREY)


def story(draw, x, y, w, kicker_text, head, text, head_size=24,
          head_leading=29, body_size=15, body_leading=21):
    y = kicker(draw, kicker_text, x, y)
    y = headline(draw, head, font(SERIF_B, head_size), x, y, w, head_leading)
    y = body(draw, text, x, y + 2, w, size=body_size, leading=body_leading)
    return y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="entry.png")
    args = ap.parse_args()

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    y = 30
    d.text((MARGIN, y), "THE WORLD IN ONE PAGE", font=font(SERIF_B, 58), fill=INK)
    y = 30 + 66
    y = rule(d, MARGIN, y, CW, width=4)
    y = rule(d, MARGIN, y + 2, CW, width=1)
    dateline = "TUESDAY 24 NOVEMBER 2026"
    sub = "ONE IMAGE  ·  SEVEN STORIES  ·  ALL VERIFIED"
    d.text((MARGIN, y + 4), dateline, font=font(SANS_B, 19), fill=INK)
    sw = d.textlength(sub, font=font(SANS, 16))
    d.text((MARGIN + CW - sw, y + 6), sub, font=font(SANS, 16), fill=GREY)
    y = y + 36
    y = rule(d, MARGIN, y, CW, width=2)

    # ---- Lead story: Riyadh --------------------------------------------
    y += 10
    y = kicker(d, "Middle East — Lead story", MARGIN, y, size=16)
    y = headline(d, "DRONE STRIKES RIYADH TOWER, 11 HURT",
                 font(SERIF_B, 38), MARGIN, y, CW, 44)
    y = body(d, "A drone attack hit the PIF Tower in Riyadh's financial district on "
                "Tuesday, injuring 11 people, Saudi civil defence said. It was the "
                "second strike on the capital in under a week, claimed by Yemen's "
                "Houthis, who said the tower was the target.",
             MARGIN, y + 2, CW, size=17, leading=24)
    y += 8
    skyline(d, MARGIN, y, CW, 76)
    y += 76 + 16
    y = rule(d, MARGIN, y, CW, width=2)

    # ---- Two-column middle ----------------------------------------------
    col_w = (CW - 24) // 2
    left_x, right_x = MARGIN, MARGIN + col_w + 24
    y_mid = y + 12
    ly = story(d, left_x, y_mid, col_w,
               "Technology — Law",
               "Huawei guilty of trade secrets theft",
               "A US jury found Huawei guilty of conspiracy to steal trade secrets "
               "and bank fraud, but acquitted the Chinese firm of the more serious "
               "racketeering charge.")
    ly = rule(d, left_x, ly + 8, col_w, width=1)
    ly = story(d, left_x, ly + 10, col_w,
               "Sport — Football",
               "Senegal win back Africa Cup title",
               "The Court of Arbitration for Sport returned the 2025 Africa Cup of "
               "Nations title to Senegal, overturning a ruling that had handed the "
               "trophy to Morocco after a chaotic final.")
    ry = story(d, right_x, y_mid, col_w,
               "Americas — Colombia",
               "Gunmen seize shoppers in Cartagena",
               "Masked gunmen took about 30 people hostage at an Exito supermarket "
               "in Cartagena, Colombia, after a failed raid on an armoured truck, "
               "police said.")
    ry = rule(d, right_x, ry + 8, col_w, width=1)
    ry = story(d, right_x, ry + 10, col_w,
               "Europe — Turkiye",
               "Five killed in army helicopter crash",
               "A Turkish Air Force helicopter crashed shortly after take-off from "
               "Eskisehir on a training flight, killing all five crew members, the "
               "defence ministry said.")
    y = max(ly, ry) + 10
    y = rule(d, MARGIN, y, CW, width=2)

    # ---- Bottom band -----------------------------------------------------
    y += 12
    by = story(d, left_x, y, col_w,
               "War in Ukraine",
               "Ukraine hits Russian ships at sea",
               "Ukraine said its drones struck the Russian cargo ship Sparta II in "
               "the Gulf of Finland and another vessel off Libya, widening the war "
               "at sea.")
    story(d, right_x, y, col_w,
          "Sport — Champions League",
          "Madrid fight back to rout PSV 5-1",
          "Real Madrid came from a goal down to beat PSV 5-1 in the Champions "
          "League. Jude Bellingham scored a stunning volley and Kylian Mbappe "
          "netted twice.")
    y = max(by, y) + 0
    # bottom band ends around y + ~150; place footer rule near bottom
    fy = 950
    rule(d, MARGIN, fy, CW, width=2)
    d.text((MARGIN, fy + 9),
           "Sources: Al Jazeera · BBC · Associated Press · CNN · Turkish Ministry of National Defence ·",
           font=font(SANS, 13), fill=GREY)
    d.text((MARGIN, fy + 27),
           "Reuters — all stories reported 24 November 2026. Image drawn entirely in code; no photographs.",
           font=font(SANS, 13), fill=GREY)

    img.save(args.output, format="PNG")
    print(f"Wrote {args.output} ({W}x{H})")


if __name__ == "__main__":
    sys.exit(main())
