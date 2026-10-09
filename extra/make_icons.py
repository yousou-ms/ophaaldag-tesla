import sys
from PIL import Image, ImageDraw

out = sys.argv[1]
BG = (36, 87, 168)      # staalblauw
OK = (255, 255, 255)
LINE = (180, 205, 240)

def draw(size, maskable=False, radius_ratio=0.22):
    s = 4 * size  # supersample
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if maskable:
        d.rectangle([0, 0, s, s], fill=BG)
        pad = s * 0.2
    else:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * radius_ratio), fill=BG)
        pad = s * 0.12
    inner = s - 2 * pad
    # klembord: lijst met drie regels, bovenste met vinkje
    x0, y0 = pad + inner * 0.08, pad + inner * 0.10
    w = inner * 0.84
    row_h = inner * 0.27
    for i in range(3):
        y = y0 + i * row_h
        box = inner * 0.17
        bx, by = x0, y + (row_h - box) / 2 - row_h * 0.05
        lw = max(2, int(s * 0.018))
        d.rounded_rectangle([bx, by, bx + box, by + box], radius=int(box * 0.22), outline=OK, width=lw)
        if i < 2:
            # vinkje
            pts = [(bx + box * 0.2, by + box * 0.52), (bx + box * 0.43, by + box * 0.75), (bx + box * 0.82, by + box * 0.25)]
            d.line(pts, fill=OK, width=int(lw * 1.5), joint="curve")
        lx = bx + box + inner * 0.08
        ly = by + box / 2
        d.rounded_rectangle([lx, ly - lw, x0 + w, ly + lw], radius=lw, fill=LINE if i < 2 else OK)
    return img.resize((size, size), Image.LANCZOS)

draw(192).save(f"{out}/icon-192.png")
draw(512).save(f"{out}/icon-512.png")
draw(512, maskable=True).save(f"{out}/icon-maskable-512.png")
# Apple voegt zelf afgeronde hoeken toe: vierkant, geen transparantie
a = draw(180, maskable=True).convert("RGB")
a.save(f"{out}/apple-touch-icon.png")
print("ok")
