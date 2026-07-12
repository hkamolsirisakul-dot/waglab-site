# thewaglabco.com

Marketing site for **The Wag Lab Co** — the umbrella company; **Pawma** is the first product.

Static, self-contained, hosted on GitHub Pages. No Manus, no build server, no lock-in.

## Files
- `index.html` — the deployable site. Fully self-contained (screenshots inlined as WebP data URIs). This is what GitHub Pages serves.
- `template.html` — editable source. Copy and layout live here, with `{{PLACEHOLDER}}` slots for images.
- `build.py` — recompresses the Pawma App Store screenshots and injects them into `template.html` → `index.html`.

## Editing
1. Edit copy/layout in `template.html`.
2. `python3 build.py` (needs Pillow: `pip3 install Pillow`).
3. Commit `index.html` — GitHub Pages redeploys automatically.

For pure text edits you can also edit `index.html` directly; just keep `template.html` in sync.

## Domain
Custom domain: `thewaglabco.com` (set in repo Settings → Pages once DNS is pointed at GitHub).
