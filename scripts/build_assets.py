#!/usr/bin/env python3
"""Build the profile README artwork (hero banner, typing line, proof strip) in dark and light.

Every graphic is a committed SVG: no third-party image service can break the profile.
Fonts: system UI stack only (GitHub's image proxy blocks web fonts).
Animation: CSS @keyframes only (GitHub strips scripts and SMIL is unreliable).
Run: python3 scripts/build_assets.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif"

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

# Design language D-corrected (plan v2, Addition 2): flat surfaces, hairlines, ONE teal accent, no gradients.
THEMES = {
    "dark": dict(bg="#111615", bg2="#111615", surface="#171D1C", ink="#E7EEEC", quiet="#AEB9B6",
                 teal="#4FC3B6", chip_bg="#16302D", chip_ink="#9FE3DA", rule="#2C3634"),
    "light": dict(bg="#F6F8F7", bg2="#F6F8F7", surface="#FFFFFF", ink="#16201E", quiet="#47524F",
                  teal="#0E7C74", chip_bg="#E2F2EF", chip_ink="#0B5F59", rule="#D5DDDB"),
}

# Before → after, drawn to scale (outline = before, filled = after). Verified, TECH_PROFILE_MASTER v11.
BULLETS = [
    ("Heartbeat tokens a day", 12.0, 1.0, "12.0 M", "1.0 M"),
    ("Memory search latency", 48, 2.8, "48 s", "2.8 s"),
    ("Gateway CPU", 209, 4, "209%", "4%"),
    ("Critical security findings", 8, 0, "8", "0"),
    ("Extraction cost per message", 38, 4, "~38k tok", "~4k tok"),
]

# Verified claims only (TECH_PROFILE_MASTER v11, evidence tag ✅)
PROOF = [
    ("626", "commits · Empire OS"),
    ("2", "production AI platforms"),
    ("24", "production agents"),
    ("99/99", "release-gate suites"),
    ("−91%", "heartbeat token spend"),
    ("20 yrs", "clinical & hospital ops"),
]

TYPING = [
    "Architect of 24 production AI agents",
    "Cut LLM heartbeat spend by 91%",
    "20 years running hospitals and clinics",
    "DICOM → 3D-printed surgical models",
]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def hero(t: dict) -> str:
    chips = ["Health-tech AI", "Forward-deployed AI engineering", "AI governance"]
    x, chip_svg = 72, []
    for c in chips:
        w = 18 + int(len(c) * 8.6)
        chip_svg.append(
            f'<g class="chip"><rect x="{x}" y="238" width="{w}" height="34" rx="4" fill="{t["chip_bg"]}"/>'
            f'<text x="{x + w / 2}" y="260" text-anchor="middle" font-size="15" font-weight="600" fill="{t["chip_ink"]}">{esc(c)}</text></g>')
        x += w + 12
    nodes = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{t["teal"]}" opacity="{o}"/>'
        for cx, cy, r, o in [(1040, 90, 7, .9), (1130, 150, 5, .7), (1010, 200, 6, .8), (1180, 70, 4, .6),
                             (1100, 250, 5, .7), (1200, 210, 7, .9), (960, 130, 4, .6)])
    links = "".join(
        f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="{t["teal"]}" stroke-width="1.2" opacity=".35"/>'
        for a, b, c, d in [(1040, 90, 1130, 150), (1130, 150, 1010, 200), (1040, 90, 1180, 70), (1130, 150, 1200, 210),
                           (1010, 200, 1100, 250), (1100, 250, 1200, 210), (960, 130, 1040, 90), (960, 130, 1010, 200)])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="320" viewBox="0 0 1280 320" role="img" aria-label="Dr. Ravi Teja Thiriveedhi — clinician turned AI systems architect">
<style>
 text{{font-family:{FONT}}}
 .in{{opacity:0;animation:in .9s ease-out forwards}}
 .d1{{animation-delay:.15s}} .d2{{animation-delay:.45s}} .d3{{animation-delay:.75s}}
 .net circle{{animation:pulse 3.2s ease-in-out infinite}}
 .net circle:nth-child(2n){{animation-delay:1.1s}} .net circle:nth-child(3n){{animation-delay:2s}}
 @keyframes in{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
 @keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
 @media (prefers-reduced-motion:reduce){{.in{{opacity:1;animation:none}} .net circle{{animation:none}}}}
</style>
<rect x="1" y="1" width="1278" height="318" rx="6" fill="{t["surface"]}" stroke="{t["rule"]}"/>
<text class="in d1" x="72" y="62" font-family="{MONO}" font-size="13" letter-spacing="1.6" fill="{t["teal"]}">CLINICIAN → AI SYSTEMS ARCHITECT</text>
<g class="net">{links}{nodes}</g>
<text class="in d1" x="72" y="108" font-size="44" font-weight="700" fill="{t["ink"]}">Dr. Ravi Teja Thiriveedhi</text>
<text class="in d2" x="72" y="154" font-size="24" font-weight="600" fill="{t["ink"]}">I build, govern and cost-engineer production multi-agent AI.</text>
<text class="in d2" x="72" y="196" font-size="18" fill="{t["quiet"]}">Twenty years of clinical practice and hospital operations behind every design decision.</text>
<g class="in d3">{"".join(chip_svg)}</g>
<text x="1208" y="296" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="1" fill="{t["quiet"]}">Hyderabad, India · Remote (IST, UTC+5:30)</text>
</svg>
'''


def typing(t: dict) -> str:
    n, dur = len(TYPING), 12
    slot = 100 / n
    parts = []
    for i, line in enumerate(TYPING):
        a, b = i * slot, (i + 1) * slot
        parts.append(f'.l{i}{{animation:f{i} {dur}s linear infinite}}'
                     f'@keyframes f{i}{{0%,{a:.2f}%{{opacity:0}}{a + 2:.2f}%,{b - 3:.2f}%{{opacity:1}}{b - 1:.2f}%,100%{{opacity:0}}}}')
    texts = "".join(
        f'<text class="l{i}" x="400" y="34" text-anchor="middle" font-size="22" font-weight="600" fill="{t["teal"]}">{esc(s)}</text>'
        for i, s in enumerate(TYPING))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="50" viewBox="0 0 800 50" role="img" aria-label="{esc(" · ".join(TYPING))}">
<style>text{{font-family:{FONT};opacity:0}}{"".join(parts)}
@media (prefers-reduced-motion:reduce){{text{{animation:none!important}} .l0{{opacity:1}}}}</style>
{texts}
</svg>
'''


def proof(t: dict) -> str:
    w, h, cols = 1280, 120, len(PROOF)
    cw = (w - 48) / cols
    cells = []
    for i, (num, label) in enumerate(PROOF):
        cx = 24 + cw * i + cw / 2
        sep = (f'<line x1="{24 + cw * i}" y1="28" x2="{24 + cw * i}" y2="92" stroke="{t["rule"]}"/>' if i else "")
        cells.append(f'{sep}<text x="{cx}" y="62" text-anchor="middle" font-size="34" font-weight="700" fill="{t["teal"]}">{esc(num)}</text>'
                     f'<text x="{cx}" y="90" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{t["quiet"]}">{esc(label.upper())}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(" · ".join(n + " " + l for n, l in PROOF))}">
<style>text{{font-family:{FONT}}}</style>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="6" fill="{t["surface"]}" stroke="{t["rule"]}"/>
{"".join(cells)}
</svg>
'''


def bullets(t: dict) -> str:
    w, row, top = 1280, 64, 96
    h = top + row * len(BULLETS) + 16
    x0, x1 = 420, 1080
    rows = []
    for i, (label, before, after, bl, al) in enumerate(BULLETS):
        y = top + i * row
        scale = (x1 - x0) / before
        bw, aw = before * scale, max(after * scale, 2)
        rows.append(
            f'<text x="56" y="{y + 22}" font-size="17" font-weight="600" fill="{t["ink"]}">{esc(label)}</text>'
            f'<rect x="{x0}" y="{y + 6}" width="{bw:.1f}" height="22" rx="2" fill="none" stroke="{t["quiet"]}" stroke-width="1.2"/>'
            f'<rect class="bar" style="animation-delay:{.15 * i:.2f}s" x="{x0}" y="{y + 10}" width="{aw:.1f}" height="14" rx="2" fill="{t["teal"]}"/>'
            f'<text x="{x1 + 20}" y="{y + 22}" font-family="{MONO}" font-size="13" fill="{t["quiet"]}">{esc(bl)} → <tspan fill="{t["teal"]}" font-weight="700">{esc(al)}</tspan></text>'
            f'<line x1="56" y1="{y + row - 14}" x2="{w - 56}" y2="{y + row - 14}" stroke="{t["rule"]}"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Measured, not claimed: {esc("; ".join(f"{l} {b} to {a}" for l, _, _, b, a in BULLETS))}">
<style>text{{font-family:{FONT}}} .bar{{transform-box:fill-box;transform-origin:left;animation:grow 1.1s ease-out both}}
@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
@media (prefers-reduced-motion:reduce){{.bar{{animation:none}}}}</style>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="6" fill="{t["surface"]}" stroke="{t["rule"]}"/>
<text x="56" y="48" font-family="{MONO}" font-size="12" letter-spacing="1.6" fill="{t["teal"]}">MEASURED, NOT CLAIMED</text>
<text x="56" y="74" font-size="15" fill="{t["quiet"]}">Outline = before · filled = after · each row drawn to its own scale from live systems</text>
{"".join(rows)}
</svg>
'''


for name, t in THEMES.items():
    (OUT / f"bullets-{name}.svg").write_text(bullets(t), encoding="utf-8")
    (OUT / f"hero-{name}.svg").write_text(hero(t), encoding="utf-8")
    (OUT / f"typing-{name}.svg").write_text(typing(t), encoding="utf-8")
    (OUT / f"proof-{name}.svg").write_text(proof(t), encoding="utf-8")
print("built:", sorted(p.name for p in OUT.glob("*.svg")))
