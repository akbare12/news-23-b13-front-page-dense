#!/usr/bin/env python3
"""THE WORLD TODAY - Monday 23 November 2026. Dense front page, 31 stories."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 236)
INK = (20, 20, 20)
RED = (178, 34, 34)
DARK = (18, 18, 18)
GOLD = (201, 162, 39)
CREAM = (250, 246, 232)
NAVY = (16, 32, 64)
TEAL = (14, 90, 96)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, fnt, fill, maxw, lh, max_lines=None):
    lines = wrap(d, text, fnt, maxw)
    if max_lines:
        lines = lines[:max_lines]
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=fnt, fill=fill)
    return y + len(lines) * lh


def chip(d, x, y, label, bg, fg=(255, 255, 255)):
    f = font(F_SANSB, 10)
    w = d.textlength(label, font=f) + 10
    d.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=bg)
    d.text((x + 5, y + 2), label, font=f, fill=fg)
    return w


def draw_map(d, x0, y0, mw, mh):
    """Simplified world map, equirectangular lon/lat -> box."""
    def proj(lon, lat):
        return (x0 + (lon + 180) / 360.0 * mw, y0 + (90 - lat) / 180.0 * mh)

    NA = [(-168, 66), (-140, 70), (-120, 71), (-95, 80), (-80, 73), (-60, 60),
          (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
          (-105, 20), (-110, 23), (-120, 34), (-125, 40), (-125, 49),
          (-140, 60), (-155, 58), (-165, 60)]
    SA = [(-80, 10), (-77, 4), (-80, -3), (-81, -6), (-70, -18), (-70, -30),
          (-70, -40), (-65, -55), (-60, -50), (-55, -35), (-48, -28),
          (-40, -20), (-35, -8), (-45, -3), (-55, 0), (-62, 5), (-72, 10)]
    EU = [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
          (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (25, 65),
          (20, 70), (15, 68), (10, 62), (5, 58), (-2, 55), (-5, 50), (-10, 43)]
    AF = [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12),
          (51, 11), (48, 0), (40, -10), (35, -20), (32, -28), (28, -33),
          (20, -35), (15, -27), (12, -18), (9, -2), (9, 4), (-8, 4),
          (-15, 11), (-17, 15), (-16, 20), (-10, 31)]
    AS = [(30, 36), (36, 36), (40, 30), (45, 29), (50, 29), (55, 26),
          (57, 25), (60, 25), (66, 25), (70, 22), (75, 20), (80, 15),
          (80, 8), (85, 20), (90, 22), (95, 16), (100, 8), (103, 2),
          (105, 10), (109, 15), (108, 20), (115, 23), (120, 28), (122, 32),
          (127, 35), (130, 38), (135, 42), (140, 45), (142, 50), (140, 55),
          (158, 52), (162, 58), (170, 60), (178, 65), (170, 66), (160, 69),
          (140, 72), (120, 73), (110, 74), (100, 76), (80, 73), (68, 68),
          (60, 68), (50, 68), (40, 67), (35, 66), (32, 70)]
    AU = [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32),
          (132, -32), (135, -35), (140, -38), (145, -38), (150, -37),
          (153, -32), (153, -27), (150, -22), (146, -19), (142, -15),
          (142, -11), (137, -12), (135, -15), (132, -12), (130, -13),
          (126, -14), (122, -17), (118, -20)]
    GL = [(-45, 60), (-30, 60), (-25, 65), (-20, 70), (-25, 75), (-40, 78),
          (-55, 76), (-58, 70), (-55, 64)]
    for poly in (NA, SA, EU, AF, AS, AU, GL):
        d.polygon([proj(lo, la) for lo, la in poly], fill=(168, 196, 138),
                  outline=(120, 150, 100))
    # grid
    for lon in range(-150, 181, 30):
        gx = x0 + (lon + 180) / 360.0 * mw
        d.line([gx, y0, gx, y0 + mh], fill=(200, 210, 200), width=1)
    for lat in range(-60, 91, 30):
        gy = y0 + (90 - lat) / 180.0 * mh
        d.line([x0, gy, x0 + mw, gy], fill=(200, 210, 200), width=1)
    return proj


def pin(d, proj, lon, lat, n, dx=0, dy=0):
    x, y = proj(lon, lat)
    x += dx
    y += dy
    f = font(F_SANSB, 9)
    tw = d.textlength(str(n), font=f)
    r = max(8, tw / 2 + 3)
    d.ellipse([x - r, y - 8, x + r, y + 8], fill=RED, outline=(255, 255, 255), width=2)
    d.text((x - tw / 2, y - 6), str(n), font=f, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 62], fill=DARK)
    d.text((12, 10), "THE WORLD TODAY", font=font(F_SERIF, 38), fill=(255, 255, 255))
    d.text((W - 12 - d.textlength("MONDAY 23 NOVEMBER 2026", font=font(F_SANSB, 20)),
            20), "MONDAY 23 NOVEMBER 2026", font=font(F_SANSB, 20), fill=GOLD)

    # ---- Kicker ----
    d.text((12, 66), "AI rout hits Asia  ·  UN chief urges AI rules  ·  US lead over China at record low  ·  Anthropic IPO $107.3B",
           font=font(F_SANS, 13), fill=RED)

    # ---- Number strip ----
    nums = [("-3.3%", "KOSPI", NAVY), ("5.3", "US-CHINA POWER GAP", (120, 90, 0)),
            ("11,762", "EBOLA CASES, DRC", (120, 60, 0)), ("$450M", "SKUBAL DEAL", (0, 110, 60)),
            ("$107.3B", "ANTHROPIC IPO", (110, 40, 120))]
    cw = W / 5
    for i, (v, lab, col) in enumerate(nums):
        x = i * cw
        d.text((x + 14, 88), v, font=font(F_SANSB, 26), fill=col)
        d.text((x + 14, 116), lab, font=font(F_SANSB, 10), fill=(90, 90, 90))
        if i:
            d.line([x, 90, x, 124], fill=(200, 200, 190), width=1)

    # ---- Region bar ----
    regs = [("ASIA-PACIFIC 6", (178, 34, 34)), ("AMERICAS 8", (30, 70, 140)),
            ("MIDDLE EAST 7", (120, 90, 0)), ("EUROPE 5", (14, 90, 96)),
            ("AFRICA 3", (0, 110, 60)), ("WORLD 2", (110, 40, 120))]
    x = 8
    d.rectangle([0, 128, W, 150], fill=(30, 30, 30))
    for lab, col in regs:
        f = font(F_SANSB, 12)
        w = d.textlength(lab, font=f) + 18
        d.rectangle([x, 131, x + w, 147], fill=col)
        d.text((x + 9, 134), lab, font=f, fill=(255, 255, 255))
        x += w + 6

    # ---- Day in numbers ----
    d.rectangle([0, 150, W, 168], fill=(235, 228, 210))
    d.text((12, 154), "THE DAY IN NUMBERS", font=font(F_SANSB, 11), fill=INK)
    d.text((180, 154), "−5.8% INTRADAY LOW  ·  165 MISSILES IN A WEEK  ·  12,000 CLEARED IN MANCHESTER  ·  264 KG SEIZED IN LEBANON  ·  2% WEALTH TAX BACKED",
           font=font(F_SANS, 11), fill=(60, 60, 60))

    # ---- Heroes ----
    heroes = [
        dict(x=8, num="1", title="AI ROUT HITS ASIA",
             body="Kospi −3.3% to 4,708.54, sheds 161 pts; intraday −5.8%. Samsung −3.1%, SK Hynix −2.5% as the AI sell-off spreads from Wall Street.",
             src="KOREA EXCHANGE", chip=("REPORTED", NAVY), kind="chart"),
        dict(x=348, num="2", title="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
             body="UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework — a blueprint, not a treaty.",
             src="UNITED NATIONS", chip=("REPORTED", NAVY), kind="globe"),
        dict(x=688, num="3", title="US LEAD OVER CHINA AT RECORD LOW",
             body="Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018. US diplomatic influence −6 to 76.7; India third at 40.5.",
             src="LOWY INSTITUTE", chip=("REPORTED", NAVY), kind="bars"),
    ]
    for h in heroes:
        x, y = h["x"], 172
        w = 328
        # scene
        d.rectangle([x, y, x + w, y + 148], fill=(220, 220, 210))
        if h["kind"] == "chart":
            d.rectangle([x, y, x + w, y + 148], fill=NAVY)
            # skyline
            import random
            rnd = random.Random(7)
            bx = x + 6
            while bx < x + w - 20:
                bw = rnd.randint(18, 34)
                bh = rnd.randint(30, 80)
                d.rectangle([bx, y + 148 - bh, bx + bw, y + 148], fill=(10, 20, 45))
                for wy in range(y + 148 - bh + 6, y + 140, 12):
                    for wx in range(bx + 4, bx + bw - 4, 9):
                        if rnd.random() < 0.5:
                            d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 90))
                bx += bw + 4
            pts = [(x + 14 + i * 34, y + 22 + i * 11 + (6 if i % 2 else 0)) for i in range(10)]
            d.line(pts, fill=(255, 70, 60), width=4)
            for px, py in pts:
                d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 200, 60))
            d.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] + 16, pts[-1][1] - 4),
                       (pts[-1][0] + 4, pts[-1][1] + 12)], fill=(255, 70, 60))
            d.text((x + 12, y + 6), "−3.3%", font=font(F_SANSB, 30), fill=(255, 70, 60))
            d.rectangle([x + 8, y + 122, x + 216, y + 144], fill=(0, 0, 0))
            d.text((x + 12, y + 126), "KOSPI  4,708.54  ·  −161 PTS",
                   font=font(F_SANSB, 12), fill=(255, 255, 255))
        elif h["kind"] == "globe":
            d.rectangle([x, y, x + w, y + 148], fill=TEAL)
            cx, cy, r = x + 240, y + 80, 42
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(140, 200, 220),
                      outline=(255, 255, 255), width=2)
            import math as _m
            for dy in (-22, 0, 22):
                hw = int(_m.sqrt(max(r * r - dy * dy, 0)))
                d.line([cx - hw, cy + dy, cx + hw, cy + dy], fill=(255, 255, 255), width=1)
            d.arc([cx - r // 2, cy - r, cx + r // 2, cy + r], 0, 360,
                  fill=(255, 255, 255), width=1)
            d.ellipse([cx - 26, cy - 26, cx - 4, cy - 8], fill=(90, 170, 90))
            d.ellipse([cx + 4, cy + 6, cx + 28, cy + 28], fill=(90, 170, 90))
            # flags
            for i, col in enumerate([(200, 40, 40), (40, 90, 200), (220, 180, 40), (40, 140, 60)]):
                fx = x + 24 + i * 26
                d.line([fx, y + 96, fx, y + 138], fill=(255, 255, 255), width=3)
                d.polygon([(fx, y + 96), (fx + 22, y + 102), (fx, y + 108)], fill=col)
            # podium
            d.polygon([(x + 120, y + 148), (x + 150, y + 108), (x + 240, y + 108),
                       (x + 268, y + 148)], fill=(120, 85, 50))
            d.text((x + 12, y + 6), "150 DELEGATES", font=font(F_SANSB, 20), fill=(255, 210, 90))
        else:
            d.rectangle([x, y, x + w, y + 148], fill=CREAM)
            d.text((x + 12, y + 8), "NARROWEST SINCE 2018",
                   font=font(F_SANSB, 13), fill=INK)
            bars = [("US", 78.9, NAVY, 78), ("CHINA", 73.6, RED, 73), ("INDIA", 40.5, (180, 140, 30), 42)]
            bx = x + 30
            for lab, val, col, bh in bars:
                d.rectangle([bx, y + 128 - bh, bx + 56, y + 128], fill=col)
                d.text((bx + 4, y + 128 - bh - 20), f"{val}", font=font(F_SANSB, 16), fill=col)
                d.text((bx + 4, y + 132), lab, font=font(F_SANSB, 11), fill=INK)
                bx += 96
            d.text((x + w - 92, y + 10), "5.3", font=font(F_SANSB, 30), fill=(180, 140, 30))
        # title + body + source
        ty = y + 156
        d.text((x, ty), h["num"], font=font(F_SANSB, 20), fill=RED)
        text_block(d, x + 22, ty + 2, h["title"], font(F_SANSB, 17), INK, w - 22, 20, max_lines=2)
        by = ty + 44
        text_block(d, x, by, h["body"], font(F_SANS, 12), (40, 40, 40), w, 14, max_lines=3)
        d.text((x, y + 246), h["src"], font=font(F_SANSB, 10), fill=(110, 110, 110))
        chip(d, x + w - 78, y + 244, h["chip"][0], h["chip"][1])

    # ---- 10 small cards ----
    cards = [
        ("4", "BESSENT DEMANDS NVIDIA ANSWERS", "Treasury chief wants to know of violations over China sales.", "REUTERS", "REPORTED", NAVY, (30, 70, 140)),
        ("5", "FBI PROBES POLICE-DATABASE HACK", "Hackers hit the NCIC system used by police nationwide.", "AP", "REPORTED", NAVY, (90, 60, 120)),
        ("6", "TRUMP: IRAN STRIKES MAY RESUME", "President says strikes could resume in the New Year.", "REUTERS", "REPORTED", NAVY, (140, 40, 40)),
        ("7", "US FUTURES JUMP 3%", "Holiday-week rally lifts Nasdaq futures as the AI rout cools.", "BLOOMBERG", "REPORTED", NAVY, (0, 110, 60)),
        ("8", "SKUBAL'S $450M METS DEAL", "Two-time Cy Young winner signs nine years, a pitcher record.", "ESPN", "REPORTED", NAVY, (120, 90, 0)),
        ("9", "TOM JACKSON DIES AT 75", "Broncos linebacker turned ESPN voice dies.", "ESPN", "REPORTED", NAVY, (60, 60, 60)),
        ("10", "STATES SUE SPACEX", "Ten states challenge AI safety claims.", "AP", "REPORTED", NAVY, (120, 90, 40)),
        ("11", "ANTHROPIC IPO: $107.3B", "Claude maker raises at $83 a share; debut closes $97.17.", "WSJ", "REPORTED", NAVY, (90, 40, 120)),
        ("12", "POLAND: 3 RUSSIAN MISSILES CROSSED AIRSPACE", "Kyiv says three Kh-101s crossed Polish airspace Friday.", "AP", "CLAIM", RED, (140, 40, 40)),
        ("13", "RUSSIAN NUCLEAR SATELLITE", "Intel claims Moscow built a satellite to carry a warhead.", "REUTERS", "CLAIM", RED, (40, 40, 90)),
    ]
    for i, (num, title, body, src, clab, ccol, band) in enumerate(cards):
        cx = 8 + (i % 5) * 202
        cy = 436 + (i // 5) * 100
        cw2 = 196
        d.rectangle([cx, cy, cx + cw2, cy + 94], fill=(255, 255, 255),
                    outline=(200, 200, 190))
        d.rectangle([cx, cy, cx + cw2, cy + 18], fill=band)
        d.text((cx + 6, cy + 3), num, font=font(F_SANSB, 12), fill=(255, 255, 255))
        # tiny icon: bars
        for k in range(3):
            d.rectangle([cx + cw2 - 30 + k * 7, cy + 14 - k * 3, cx + cw2 - 26 + k * 7, cy + 14],
                        fill=(255, 255, 255))
        text_block(d, cx + 6, cy + 22, title, font(F_SANSB, 12), INK, cw2 - 12, 14, max_lines=2)
        text_block(d, cx + 6, cy + 52, body, font(F_SANS, 10.5), (60, 60, 60), cw2 - 12, 12, max_lines=2)
        d.text((cx + 6, cy + 79), src, font=font(F_SANSB, 9), fill=(130, 130, 130))
        chip(d, cx + cw2 - 72, cy + 77, clab, ccol)

    # ---- Map + ALSO ----
    d.text((8, 640), "WHERE IT HAPPENED", font=font(F_SANSB, 13), fill=INK)
    d.text((588, 640), "ALSO ON MONDAY", font=font(F_SANSB, 13), fill=INK)
    d.rectangle([8, 660, 576, 856], fill=(225, 235, 225), outline=(180, 190, 180))
    proj = draw_map(d, 8, 660, 568, 196)
    pins = [(127, 37.5, 1), (-59.6, 13.1, 2), (116.4, 39.9, 3), (-77, 38.9, 4),
            (-74, 40.7, "5·8"), (51.4, 35.7, 6), (-87.6, 41.9, 7),
            (-105, 39.7, 9), (-97.7, 30.3, 10), (-122.4, 37.8, 11),
            (21, 52.2, 12), (37.6, 55.8, 13)]
    for lon, lat, n in pins:
        pin(d, proj, lon, lat, n)
    d.text((8, 858), "Pins 1–13: 1 Seoul · 2 Bridgetown · 3 Beijing · 4 Washington · 5·8 New York · 6 Tehran",
           font=font(F_SANS, 9), fill=(70, 70, 70))
    d.text((8, 870), "7 Chicago · 9 Denver · 10 Austin · 11 San Francisco · 12 Warsaw · 13 Moscow",
           font=font(F_SANS, 9), fill=(70, 70, 70))

    also = [
        ("14", "Paris: 100+ back 2% wealth tax"),
        ("15", "Manchester: 12,000 cleared"),
        ("16", "Zelenskyy: 165 missiles in a week"),
        ("17", "COP31: day after pact rejected"),
        ("18", "Benghazi: UN demands port probe"),
        ("19", "Israel unity talks resume"),
        ("20", "Gaza: two killed in Israeli strike"),
        ("21", "West Bank settler attacks"),
        ("22", "Iran war: no deal in sight"),
        ("23", "Lebanon seizes 264 kg explosives"),
        ("24", "Bahrain: strike hits plant, 2 hurt"),
        ("25", "Sudan: defences down drones"),
        ("26", "DRC: fighting traps Ebola teams"),
        ("27", "Bangladesh: Hasina jailed if returns"),
        ("28", "Seoul minister quits over exam chaos"),
        ("29", "SK Telecom −7.3% as hype cools"),
        ("30", "China eases margin rules"),
        ("31", "Seoul readies 10T-won fund"),
    ]
    for i, (num, txt) in enumerate(also):
        ax = 588 + (i // 9) * 214
        ay = 662 + (i % 9) * 24
        d.text((ax, ay), num + ".", font=font(F_SANSB, 11), fill=RED)
        text_block(d, ax + 26, ay, txt, font(F_SANS, 11), INK, 184, 12, max_lines=2)

    # ---- DATE CHECK ----
    d.rectangle([8, 884, 1016, 958], outline=RED, width=2, fill=(255, 240, 240))
    d.text((16, 890), "DATE CHECK", font=font(F_SANSB, 13), fill=RED)
    d.text((120, 890), "READ 23 NOV 2026, 23:59 UTC — STORIES DATED 23 NOV ONLY",
           font=font(F_SANSB, 11), fill=INK)
    text_block(d, 16, 910,
               "LEFT OUT — NOT 23 NOV: Democrats reach 258 seats (22 Nov) · Sparta II fire (22 Nov) · El Chapo Isidro captured (22 Nov) · EU–Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov)",
               font(F_SANS, 11), INK, 984, 14, max_lines=2)
    d.text((16, 940), "NOT YET: Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff",
           font=font(F_SANS, 11), fill=INK)

    # ---- Footer ----
    d.text((8, 966), "Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · NYT · ESPN · Lowy Institute (Asia Power Index 2026).",
           font=font(F_SANS, 10), fill=(80, 80, 80))
    d.text((8, 982), "CHIPS: REPORTED = confirmed by wires · CLAIM = one side's claim, not independently confirmed · ONGOING = still developing",
           font=font(F_SANS, 10), fill=(80, 80, 80))
    d.text((8, 998), "Scenes are drawn illustrations, not photographs.  ·  THE WORLD TODAY — Monday 23 November 2026 · 31 stories · 6 regions",
           font=font(F_SANSB, 10), fill=INK)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
