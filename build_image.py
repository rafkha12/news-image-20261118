#!/usr/bin/env python3
"""Draw the news-image-20261118 entry: a newspaper front page summing up
the world's news of Wednesday 18 November 2026. All facts are from the
verified brief; no text is invented. Output: image.png (1024x1024)."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 247, 238)      # warm newsprint
INK = (22, 22, 22)           # near-black
NAVY = (20, 38, 76)          # deep navy
RED = (176, 42, 42)          # headline red
GREY = (90, 88, 82)          # muted grey
LIGHT_LINE = (190, 184, 172)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_B = f"{FONT_DIR}/liberation/LiberationSerif-Bold.ttf"
SANS_B = f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf"
SANS = f"{FONT_DIR}/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, spacing):
    """Draw lines top-left at (x, y); returns y just below the last line."""
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def draw_block(draw, x, y, max_w, text, fnt, fill, spacing, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None and len(lines) > max_lines:
        raise ValueError(f"overflow: {len(lines)} lines for {max_lines}: {text!r}")
    return draw_lines(draw, x, y, lines, fnt, fill, spacing), lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Outer frame
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    d.rectangle([16, 16, W - 17, H - 17], outline=LIGHT_LINE, width=1)

    # ---- Masthead ----
    mast = font(SERIF_B, 96)
    d.text((W // 2, 26), "THE WORLD", font=mast, fill=INK, anchor="ma")
    # Double rule under masthead
    d.line([(36, 130), (W - 36, 130)], fill=INK, width=4)
    d.line([(36, 136), (W - 36, 136)], fill=INK, width=1)

    # ---- Date band (navy, unmistakable) ----
    d.rectangle([36, 146, W - 36, 184], fill=NAVY)
    date_f = font(SANS_B, 30)
    d.text((W // 2, 165), "WEDNESDAY, 18 NOVEMBER 2026",
           font=date_f, fill=(255, 255, 255), anchor="mm")

    # ---- Lead story ----
    lx, ly = 40, 196
    lw = 700  # text column width; globe sits to the right
    kick = font(SANS_B, 22)
    d.text((lx, ly), "MIDDLE EAST", font=kick, fill=RED)
    head = font(SERIF_B, 46)
    y = ly + 30
    y, _ = draw_block(d, lx, y, lw,
                      "IRAN STRIKES US BASES IN KUWAIT AND BAHRAIN",
                      head, INK, 2, max_lines=3)
    y += 6
    deck = font(SANS, 22)
    y, _ = draw_block(d, lx, y, lw,
                      "Drones hit Ali Al Salem Air Base in Kuwait and "
                      "Bahrain, home of the US Fifth Fleet, after a US "
                      "strike on a missile site on Qeshm Island.",
                      deck, INK, 4, max_lines=3)
    y += 6
    y, _ = draw_block(d, lx, y, lw,
                      "An ADNOC tanker was attacked in the Strait of "
                      "Hormuz \u2014 11 crew injured, 1 missing.",
                      deck, INK, 4, max_lines=2)
    lead_bottom = y

    # Globe graphic, right of the lead (abstract: navy disc, white arcs)
    cx, cy, r = 862, 330, 88
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    for frac in (0.35, 0.7):  # meridians: vertical ellipses
        w = int(r * frac)
        d.ellipse([cx - w, cy - r, cx + w, cy + r],
                  outline=(255, 255, 255), width=2)
    for frac in (-0.5, 0, 0.5):  # parallels
        yy = cy + int(r * frac)
        half = int((r * r - (r * frac) ** 2) ** 0.5)
        d.line([(cx - half, yy), (cx + half, yy)], fill=(255, 255, 255), width=2)
    # Red marker dots on the disc
    for dx, dy in ((28, -18), (44, 6), (18, 26)):
        d.ellipse([cx + dx - 5, cy + dy - 5, cx + dx + 5, cy + dy + 5],
                  fill=RED, outline=(255, 255, 255), width=2)
    cap = font(SANS_B, 16)
    d.text((cx, cy + r + 10), "THE GULF, WEDNESDAY", font=cap, fill=GREY, anchor="ma")

    # Rule under lead
    d.line([(36, 476), (W - 36, 476)], fill=INK, width=3)

    # ---- 2x2 story grid ----
    stories = [
        ("APEC \u00b7 SHENZHEN", NAVY, "XI AND PUTIN MEET IN SHENZHEN",
         "At the APEC summit; a trilateral meeting with Trump is set for "
         "Thursday. Xi spoke against trade protectionism; Putin criticised "
         "sanctions."),
        ("UKRAINE", RED, "UKRAINE HITS THE KERCH BRIDGE",
         "Drones and missiles partly destroyed the bridge to Crimea; one of "
         "its two arches collapsed into the strait."),
        ("US ELECTION", NAVY, "PELTOLA WINS ALASKA",
         "Democrat Mary Peltola beat Republican incumbent Dan Sullivan; "
         "Democrats take a 56\u201344 Senate majority."),
        ("SPACE", NAVY, "VOYAGER 1 REACHES ONE LIGHT-DAY",
         "About 16 billion miles from Earth at 5:16 a.m. ET \u2014 the first "
         "human-made object to reach that distance."),
    ]
    grid_top, grid_left = 488, 40
    col_w, row_h, gutter = 464, 176, 16
    k_f = font(SANS_B, 19)
    h_f = font(SERIF_B, 34)
    b_f = font(SANS, 20)
    for i, (kicker, kc, headline, body) in enumerate(stories):
        col = i % 2
        row = i // 2
        x = grid_left + col * (col_w + gutter)
        y = grid_top + row * row_h
        if col == 1:
            d.line([(x - gutter // 2, y + 4), (x - gutter // 2, y + row_h - 12)],
                   fill=LIGHT_LINE, width=1)
        d.text((x, y), kicker, font=k_f, fill=kc)
        y2 = y + 27
        y2, _ = draw_block(d, x, y2, col_w, headline, h_f, INK, 1, max_lines=2)
        y2 = y + 27 + 2 * (h_f.size + 1) + 4  # fixed body start: below 2 headline lines
        draw_block(d, x, y2, col_w, body, b_f, INK, 2, max_lines=3)

    # Rule above the strip
    d.line([(36, 848), (W - 36, 848)], fill=INK, width=3)

    # ---- ALSO TODAY strip ----
    d.rectangle([36, 858, W - 36, 972], fill=(30, 30, 30))
    d.text((56, 868), "ALSO TODAY", font=font(SANS_B, 22), fill=(255, 255, 255))
    strip_items = [
        "US loses measles-free status after 26 years \u2014 5,412 cases in 2026",
        "Ebola in DR Congo passes 11,000 cases",
        "Nvidia posts a record $115.8B quarter",
        "NSA outage hits its Middle East intel hub \u2014 officials say not a cyberattack",
    ]
    s_f = font(SANS, 18)
    sw = 440
    for i, item in enumerate(strip_items):
        col = i % 2
        row = i // 2
        x = 56 + col * (sw + 16)
        y = 894 + row * 36
        d.rectangle([x, y + 3, x + 10, y + 13], fill=RED)
        draw_block(d, x + 18, y, sw - 18, item, s_f, (235, 235, 235), 2,
                   max_lines=2)

    # ---- Footer (one line) ----
    foot = font(SANS, 17)
    d.text((W // 2, 984),
           "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 CNN \u00b7 NASA \u2014 "
           "Every story on this page happened on Wednesday, 18 November 2026.",
           font=foot, fill=GREY, anchor="ma")

    img.save("image.png", optimize=True)
    print(f"saved image.png; lead text ends at y={lead_bottom}")


if __name__ == "__main__":
    main()
