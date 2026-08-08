#!/usr/bin/env python3
"""Inline images from ./assets into template.html -> index.html (one portable file).

Source pet photos + app screenshots + the Pawma icon live in ./assets (committed to
the repo). The favicon (assets/pawma-icon.png) and social card (og-image.jpg) are
referenced as static files, not inlined, because og:image must be a real URL.
"""
import base64, io, pathlib
from PIL import Image

HERE = pathlib.Path(__file__).parent
ASSETS = HERE / "assets"

def webp_bytes_uri(path):
    """Inline an already-optimized .webp file verbatim (no re-encode)."""
    b = path.read_bytes()
    return f"data:image/webp;base64,{base64.b64encode(b).decode()}", len(b)

def png_to_webp_uri(path, width):
    im = Image.open(path).convert("RGBA")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="WEBP", quality=90, method=6)
    return f"data:image/webp;base64,{base64.b64encode(buf.getvalue()).decode()}", len(buf.getvalue())

repl = {}
total = 0

# Photos + screenshots: already-optimized webp, inline verbatim.
for key, fn in [
    ("{{HERO_COTTON}}",  "hero-cotton.webp"),
    ("{{SHOT_RECORD}}",  "shot-record.webp"),
    ("{{SHOT_SUMMARY}}", "shot-summary.webp"),
    ("{{ABOUT_COTTON}}", "about-cotton.webp"),
    ("{{ABOUT_ESTHER}}", "about-ester.webp"),
]:
    p = ASSETS / fn
    if p.exists():
        uri, size = webp_bytes_uri(p); repl[key] = uri; total += size
        print(f"  {fn}: {size//1024} KB")
    else:
        repl[key] = ""; print(f"  !! missing {fn}")

# Pawma app icon: downscale the 1024px master to a crisp 128px webp.
icon = ASSETS / "pawma-icon.png"
if icon.exists():
    uri, size = png_to_webp_uri(icon, 128); repl["{{PAWMA_ICON}}"] = uri; total += size
    print(f"  pawma-icon: {size//1024} KB")
else:
    repl["{{PAWMA_ICON}}"] = ""; print("  !! missing pawma-icon.png")

html = (HERE / "template.html").read_text()
for k, v in repl.items():
    html = html.replace(k, v)

out = HERE / "index.html"
out.write_text(html)
print(f"\nTotal inlined image payload: {total//1024} KB")
print(f"Final index.html: {len(html.encode())//1024} KB -> {out}")
