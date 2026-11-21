"""Republic of Veymora — invented passport spread, rendered with Pillow."""
import math
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 1024
MAROON = (90, 31, 36)
MAROON_STAMP = (138, 42, 42)
NAVY = (42, 74, 138)
GREEN = (42, 106, 69)
CREAM = (239, 233, 220)
PAPER = (243, 238, 226)
INK = (40, 35, 30)
GRAY = (120, 112, 100)
WHITE = (250, 248, 244)

FDIR = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    try:
        return ImageFont.truetype(FDIR + name, size)
    except Exception:
        return ImageFont.load_default()

F_TITLE = font("DejaVuSerif-Bold.ttf", 34)
F_SUB = font("DejaVuSerif.ttf", 17)
F_CAP = font("DejaVuSans.ttf", 11)
F_VAL = font("DejaVuSans-Bold.ttf", 15)
F_VAL_S = font("DejaVuSans-Bold.ttf", 13)
F_STAMP = font("DejaVuSans-Bold.ttf", 12)
F_STAMP_S = font("DejaVuSans.ttf", 10)
F_STAMP_B = font("DejaVuSans-Bold.ttf", 16)
F_MRZ = font("DejaVuSansMono-Bold.ttf", 17)
F_OBS = font("DejaVuSans.ttf", 13)
F_SIGN = font("DejaVuSerif-Italic.ttf", 24)
F_END = font("DejaVuSansMono-Bold.ttf", 12)

img = Image.new("RGB", (W, H), MAROON)
d = ImageDraw.Draw(img)

# ---- paper (two pages with gutter) ----
GUT = 512
d.rectangle([18, 18, GUT - 3, H - 18], fill=PAPER)
d.rectangle([GUT + 3, 18, W - 18, H - 18], fill=PAPER)

# guilloche: fine sine contour lines
for page_x0, page_x1 in ((18, GUT - 3), (GUT + 3, W - 18)):
    for i, off in enumerate(range(30, H - 20, 9)):
        amp = 4 + 2 * math.sin(i * 0.35)
        pts = []
        for x in range(page_x0, page_x1, 6):
            y = off + amp * math.sin((x + i * 13) / 46.0)
            pts.append((x, y))
        d.line(pts, fill=(226, 219, 203), width=1)

# gutter shadow
for i, wdt in enumerate(range(10, 0, -2)):
    shade = 210 - i * 6
    d.line([(GUT - 3 + i, 18), (GUT - 3 + i, H - 18)], fill=(shade, shade - 6, shade - 16))
    d.line([(GUT + 3 - i, 18), (GUT + 3 - i, H - 18)], fill=(shade, shade - 6, shade - 16))

def text_c(x, y, s, f, fill):
    d.text((x, y), s, font=f, fill=fill, anchor="ma")

# ================= LEFT PAGE =================
cx = 265
# emblem: lighthouse in double circle
for r, wd in ((46, 3), (38, 1)):
    d.ellipse([cx - r, 60, cx + r, 60 + 2 * r], outline=MAROON, width=wd)
d.polygon([(cx - 12, 108), (cx + 12, 108), (cx + 8, 74), (cx - 8, 74)], outline=MAROON, width=2)
d.rectangle([cx - 10, 74, cx + 10, 79], fill=MAROON)
d.line([(cx, 40), (cx - 10, 72)], fill=MAROON, width=1)
d.line([(cx, 40), (cx + 10, 72)], fill=MAROON, width=1)
d.rectangle([cx - 14, 108, cx + 14, 112], fill=MAROON)

text_c(cx, 128, "REPUBLIC OF VEYMORA", F_TITLE, MAROON)
text_c(cx, 176, "LIZARVEYR  ·  RZEPUBLIK VEYMORA", F_SUB, (140, 60, 64))
text_c(cx, 200, "MARKAZ-PASS  ·  PASSPORT", font("DejaVuSans.ttf", 13), GRAY)
d.line([(70, 232), (460, 232)], fill=MAROON, width=2)

# portrait: engraved-style face
def draw_portrait(x0, y0, pw, ph, ghost=False):
    pw, ph = pw, ph
    box = Image.new("RGB", (pw, ph), (225, 218, 202))
    bd = ImageDraw.Draw(box)
    cx0, fy = pw / 2, ph / 2
    fw, fh = pw * 0.40, ph * 0.34          # face half-size
    # hair mass behind
    bd.ellipse([cx0 - fw * 1.5, fy - fh * 1.55, cx0 + fw * 1.5, fy + fh * 1.25], fill=(52, 42, 38))
    # face oval
    bd.ellipse([cx0 - fw, fy - fh, cx0 + fw, fy + fh * 1.35], fill=(198, 178, 160))
    # neck + collar
    bd.rectangle([cx0 - fw * 0.45, fy + fh * 1.1, cx0 + fw * 0.45, ph], fill=(186, 166, 148))
    bd.polygon([(cx0 - fw * 1.15, ph), (cx0 - fw * 0.2, fy + fh * 1.18), (cx0 + fw * 0.2, fy + fh * 1.18), (cx0 + fw * 1.15, ph)], fill=(60, 52, 52))
    # eyes
    for sgn in (-1, 1):
        ex = cx0 + sgn * fw * 0.42
        ey = fy - fh * 0.18
        bd.ellipse([ex - fw * 0.22, ey - 5, ex + fw * 0.22, ey + 5], fill=(150, 132, 116))
        bd.ellipse([ex - 5, ey - 4, ex + 5, ey + 4], fill=(45, 38, 34))
        bd.line([(ex - fw * 0.26, ey - 9), (ex + fw * 0.26, ey - 7)], fill=(52, 42, 38), width=2)
    # nose
    bd.line([(cx0, fy - fh * 0.1), (cx0 - 3, fy + fh * 0.38)], fill=(150, 128, 110), width=2)
    bd.ellipse([cx0 - 6, fy + fh * 0.38, cx0 + 6, fy + fh * 0.5], outline=(140, 118, 100), width=1)
    # mouth
    bd.line([(cx0 - fw * 0.3, fy + fh * 0.72), (cx0 + fw * 0.3, fy + fh * 0.72)], fill=(120, 70, 66), width=2)
    bd.line([(cx0 - fw * 0.22, fy + fh * 0.80), (cx0 + fw * 0.22, fy + fh * 0.80)], fill=(150, 120, 108), width=1)
    # engraving hatch overlay
    for yy in range(2, ph - 2, 3):
        bd.line([(2, yy), (pw - 3, yy)], fill=(90, 76, 66), width=1)
    bd.rectangle([0, 0, pw - 1, ph - 1], outline=MAROON, width=2)
    bd.rectangle([3, 3, pw - 4, ph - 4], outline=MAROON, width=1)
    if ghost:
        box = Image.blend(box, Image.new("RGB", (pw, ph), PAPER), 0.86)
    img.paste(box, (x0, y0))

draw_portrait(58, 258, 152, 188)
text_c(134, 452, "FOTOGRAF · PHOTOGRAPH", F_CAP, GRAY)

# fields
def field(x, y, cap, val, big=True):
    d.text((x, y), cap, font=F_CAP, fill=GRAY)
    d.text((x, y + 14), val, font=F_VAL if big else F_VAL_S, fill=INK)

FX, FX2 = 238, 402
field(FX, 258, "TIP / TYPE", "P")
field(FX2, 258, "KOD / CODE", "VYR")
field(FX, 292, "PAS NR / PASSPORT NO.", "VY4471082")
field(FX, 326, "FAMAR / SURNAME", "OKHREY")
field(FX, 360, "ANVAR / GIVEN NAMES", "MARA ILVESTRINE")
field(FX, 394, "VATANAR / NATIONALITY", "VEYMORAN")
field(FX, 428, "KESH / SEX", "F")
field(FX, 462, "DUNVAR / DATE OF BIRTH", "12 APR 1981")
field(FX2, 462, "DUNVAR-ESH / PLACE OF BIRTH", "PORT KHELME", False)
field(FX, 496, "ISHAL / DATE OF ISSUE", "02 MAY 2024")
field(FX2, 496, "ISHAL-MER / DATE OF EXPIRY", "01 MAY 2034", False)
field(FX, 530, "DAFTAR / AUTHORITY", "HARBOUR REGISTRY,", False)
field(FX2, 530, "ISHAL-MER STAD / ISSUING POST", "VEL-SKERRY", False)
field(FX, 572, "SHAKH NR / PERSONAL NO.", "33 0917 55")

# signature
sig = []
for t in range(0, 200, 4):
    xx = 62 + t
    yy = 620 + 6 * math.sin(t / 18.0) + 3 * math.sin(t / 7.3) - t * 0.02
    sig.append((xx, yy))
d.line(sig, fill=(30, 40, 80), width=2)
d.text((62, 638), "Mara I. Okhrey", font=F_SIGN, fill=(30, 40, 80))
d.text((62, 668), "ILMAR / HOLDER'S SIGNATURE", font=F_CAP, fill=GRAY)

# (no ghost portrait: keeps the page clean)

# observations
d.rectangle([58, 712, 448, 786], outline=(190, 182, 166), width=1)
d.text((70, 720), "MERKAR / OBSERVATIONS", font=F_CAP, fill=GRAY)
d.text((70, 738), "Holder is a licensed coastal pilot, licence S-220.", font=F_OBS, fill=INK)
d.text((70, 756), "Storm-transit endorsement on page 5.", font=F_OBS, fill=INK)

# MRZ
d.rectangle([52, 830, 470, 900], fill=(233, 228, 214))
d.text((62, 838), "P<VYROKHREY<<MARA<ILVESTRINE<<<<<<<<<<<<<<<", font=F_MRZ, fill=INK)
d.text((62, 868), "VY44710820VY8404121F340501233091755<<<<<<04", font=F_MRZ, fill=INK)

text_c(430, 948, "VY4471082", F_CAP, GRAY)
d.text((30, 948), "2", font=F_CAP, fill=GRAY)

# ================= RIGHT PAGE =================
RX = GUT + 40
d.text((RX, 44), "VISAS", font=F_TITLE, fill=MAROON)
d.text((RX + 150, 62), "/ MARKAZ", font=F_SUB, fill=GRAY)
d.text((W - 60, 62), "5", font=F_CAP, fill=GRAY)
d.line([(RX, 100), (W - 60, 100)], fill=MAROON, width=2)

# endorsement box
d.rectangle([RX, 118, W - 60, 208], outline=NAVY, width=2)
d.text((RX + 12, 126), "STORM-TRANSIT ENDORSEMENT", font=font("DejaVuSansMono-Bold.ttf", 14), fill=NAVY)
for i, line in enumerate([
    "SKERRY CHANNEL IS CLOSED WHILE THE",
    "HARBORMASTER RAISES THE RED DOUBLE",
    "PENNANT. VALID WITH PILOT LICENCE S-220.",
]):
    d.text((RX + 12, 152 + i * 17), line, font=F_END, fill=NAVY)

# round toll stamp
st = Image.new("RGBA", (180, 180), (0, 0, 0, 0))
sd = ImageDraw.Draw(st)
sd.ellipse([6, 6, 174, 174], outline=MAROON_STAMP + (200,), width=3)
sd.ellipse([16, 16, 164, 164], outline=MAROON_STAMP + (200,), width=1)
for a in range(0, 360, 30):
    x1 = 90 + 74 * math.cos(math.radians(a)); y1 = 90 + 74 * math.sin(math.radians(a))
    x2 = 90 + 82 * math.cos(math.radians(a)); y2 = 90 + 82 * math.sin(math.radians(a))
    sd.line([(x1, y1), (x2, y2)], fill=MAROON_STAMP + (200,), width=2)
sd.text((90, 52), "PILOT TOLL", font=F_STAMP_B, fill=MAROON_STAMP + (230,), anchor="mm")
sd.text((90, 78), "9 VR · PAID", font=F_STAMP, fill=MAROON_STAMP + (230,), anchor="mm")
sd.text((90, 104), "VEL-SKERRY", font=F_STAMP_S, fill=MAROON_STAMP + (230,), anchor="mm")
sd.text((90, 124), "03 JUN 2024", font=F_STAMP_S, fill=MAROON_STAMP + (230,), anchor="mm")
st = st.rotate(8, resample=Image.BICUBIC, expand=True)
img.paste(st, (W - 240, 810), st)

# visa stamps
stamps = [
    ("VEYMORA", "DEPARTURE", "03 JUN 2024", "VEL-SKERRY", MAROON_STAMP, -2),
    ("DALTHEIM", "ARRIVAL", "03 JUN 2024", "GRYNZPOSTEN", NAVY, 2),
    ("DALTHEIM", "DEPARTURE", "21 JUN 2024", "GRYNZPOSTEN", NAVY, -3),
    ("VEYMORA", "ARRIVAL", "21 JUN 2024", "VEL-SKERRY", MAROON_STAMP, 2),
    ("SARVA", "ARRIVAL", "12 AUG 2025", "ORUN BORDER", GREEN, -2),
    ("SARVA", "DEPARTURE", "06 SEP 2025", "ORUN BORDER", GREEN, 3),
    ("VEYMORA", "ARRIVAL", "06 SEP 2025", "PORT KHELME", MAROON_STAMP, -2),
    ("MIRVOLD", "TRANSIT", "18 OCT 2025", "MIRVOLD QUAY", NAVY, 2),
]
sx0, sy0 = RX + 8, 226
for i, (place, kind, date, post, col, rot) in enumerate(stamps):
    sw, sh = 196, 96
    sx = sx0 + (i % 2) * 212 + (8 if i % 4 >= 2 else 0)
    sy = sy0 + (i // 2) * 112 + (4 if i % 2 else 0)
    s = Image.new("RGBA", (sw + 20, sh + 20), (0, 0, 0, 0))
    sd = ImageDraw.Draw(s)
    sd.rounded_rectangle([10, 10, 10 + sw, 10 + sh], radius=10, outline=col + (215,), width=3)
    sd.rounded_rectangle([16, 16, 4 + sw, 4 + sh], radius=8, outline=col + (120,), width=1)
    sd.text((10 + sw / 2, 26), place, font=F_STAMP_B, fill=col + (230,), anchor="ma")
    sd.text((10 + sw / 2, 52), kind, font=F_STAMP, fill=col + (230,), anchor="ma")
    sd.text((10 + sw / 2, 70), date, font=F_STAMP_B, fill=col + (230,), anchor="ma")
    sd.text((10 + sw / 2, 90), post, font=F_STAMP_S, fill=col + (200,), anchor="ma")
    s = s.rotate(rot, resample=Image.BICUBIC, expand=False)
    img.paste(s, (sx - 10, sy - 10), s)

# large pale-green visa box
gy = 712
d.rectangle([RX, gy, W - 60, gy + 128], fill=(226, 236, 220), outline=GREEN, width=2)
d.text((RX + 12, gy + 8), "SARVA · VISITOR VISA · SARVAN TASAVAULD", font=font("DejaVuSans-Bold.ttf", 14), fill=GREEN)
d.text((RX + 12, gy + 34), "TYPE", font=F_CAP, fill=GRAY); d.text((RX + 12, gy + 48), "C · SINGLE ENTRY", font=F_VAL_S, fill=INK)
d.text((RX + 190, gy + 34), "DURATION OF STAY", font=F_CAP, fill=GRAY); d.text((RX + 190, gy + 48), "30 DAYS", font=F_VAL_S, fill=INK)
d.text((RX + 12, gy + 74), "VALID FROM", font=F_CAP, fill=GRAY); d.text((RX + 12, gy + 88), "01 AUG 2025", font=F_VAL_S, fill=INK)
d.text((RX + 190, gy + 74), "UNTIL", font=F_CAP, fill=GRAY); d.text((RX + 190, gy + 88), "30 SEP 2025", font=F_VAL_S, fill=INK)
d.text((RX + 12, gy + 110), "ISSUED AT KHELME, 12 JUL 2025", font=F_CAP, fill=GRAY)
d.text((RX + 260, gy + 110), "FEE 40 SVR", font=F_CAP, fill=GRAY)

text_c(W - 120, 948, "VY4471082", F_CAP, GRAY)

# paper grain
import random
random.seed(7)
for _ in range(9000):
    x = random.randint(20, W - 20); y = random.randint(20, H - 20)
    if 505 <= x <= 519:
        continue
    c = img.getpixel((x, y))
    j = random.randint(-4, 4)
    img.putpixel((x, y), tuple(max(0, min(255, v + j)) for v in c))

out = os.getenv("MAKEFUN_OUTPUT_DIR", ".")
img.save("entry.png", optimize=True)
print("Saved entry.png", img.size, os.path.getsize("entry.png"), "bytes")
