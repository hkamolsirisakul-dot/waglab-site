#!/usr/bin/env python3
"""Inline compressed screenshots into template.html -> index.html (one portable file)."""
import base64, io, pathlib
from PIL import Image

HERE = pathlib.Path(__file__).parent
SHOTS = pathlib.Path("/Users/kamkamolsirisakul/Documents/Kam Co Work OS/Projects/WAG LAB /pawma-app/mobile/store-assets/ios-6.9")
ICON = pathlib.Path("/Users/kamkamolsirisakul/Documents/Kam Co Work OS/Projects/WAG LAB /pawma-app/mobile/assets/images/icon.png")
APPSTORE = "https://apps.apple.com/app/id6782536067"

def webp_uri(path, width, quality=80):
    im = Image.open(path).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="WEBP", quality=quality, method=6)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/webp;base64,{b64}", len(buf.getvalue())

def png_uri(path, width):
    im = Image.open(path).convert("RGBA")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="WEBP", quality=90, method=6)
    return f"data:image/webp;base64,{base64.b64encode(buf.getvalue()).decode()}", len(buf.getvalue())

repl = {"{{APPSTORE}}": APPSTORE}
total = 0
mapping = {
    "{{SHOT_RECORD}}":  ("02-pet-record.png", 560),
    "{{SHOT_CAPTURE}}": ("05-capture.png", 560),
    "{{SHOT_SUMMARY}}": ("04-vet-summary.png", 560),
    "{{SHOT_LABS}}":    ("03-vaccinations-labs.png", 560),
    "{{SHOT_HOME}}":    ("01-home.png", 560),
}
for key, (fn, w) in mapping.items():
    p = SHOTS / fn
    if p.exists():
        uri, size = webp_uri(p, w)
        repl[key] = uri
        total += size
        print(f"  {fn}: {size//1024} KB")
    else:
        repl[key] = ""
        print(f"  !! missing {fn}")

icon_uri, isize = png_uri(ICON, 96)
repl["{{ICON}}"] = icon_uri
total += isize
print(f"  icon: {isize//1024} KB")

# Real pet photos — Cotton (dog, hero) and Ester (cat, about). The emotional anchor.
PETS = pathlib.Path("/Users/kamkamolsirisakul/Documents/Kam Co Work OS/Projects/WAG LAB /pawma-app/mobile/assets/images")
for key, fn, w in [("{{COTTON}}", "Cotton 1.jpeg", 720), ("{{ESTER}}", "Ester 5.jpg", 640)]:
    p = PETS / fn
    if p.exists():
        uri, size = webp_uri(p, w, quality=82)
        repl[key] = uri
        total += size
        print(f"  {fn}: {size//1024} KB")
    else:
        repl[key] = ""
        print(f"  !! missing {fn}")

html = (HERE / "template.html").read_text()
for k, v in repl.items():
    html = html.replace(k, v)

out = HERE / "index.html"
out.write_text(html)
print(f"\nTotal image payload: {total//1024} KB")
print(f"Final index.html: {len(html.encode())//1024} KB -> {out}")
