#!/usr/bin/env python3
"""Generates the studio logo concepts as standalone SVG files (text converted to paths).

Usage:  python3 tools/logos.py
Output: site/assets/logos/<name>-dark.svg, <name>-light.svg, <name>-mark.svg
Requires: pip install fonttools  (and the Inter font family, OFL licensed)
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONTS = Path("/usr/share/fonts/opentype/inter")
OUT = Path(__file__).resolve().parent.parent / "site" / "assets" / "logos"
LIME, INK, PAPER = "#c4f25a", "#060807", "#efece5"


def tekst_pad(tekst, font, grootte, x, baseline, spatiering_em=0.0):
    """Return (svg path d, width) for text set in the given font, as outlines."""
    f = TTFont(FONTS / font)
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    schaal = grootte / f["head"].unitsPerEm
    pen = SVGPathPen(gs)
    cx = x
    for ch in tekst:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (schaal, 0, 0, -schaal, cx, baseline)))
        cx += hmtx[g][0] * schaal + spatiering_em * grootte
    return pen.getCommands(), cx - x - spatiering_em * grootte


def merk(naam, fg, accent, bg):
    """Each mark is drawn in a 120x120 box."""
    if naam == "duskform":
        return (f'<clipPath id="h"><rect x="0" y="0" width="120" height="70"/></clipPath>'
                f'<circle cx="60" cy="70" r="36" fill="{accent}" clip-path="url(#h)"/>'
                f'<g stroke="{fg}" stroke-width="7" stroke-linecap="round">'
                f'<path d="M22 82 H98"/><path d="M32 95 H88"/><path d="M44 108 H76"/></g>')
    if naam == "nachtwerk":
        return (f'<mask id="m"><rect width="120" height="120" fill="#fff"/><circle cx="76" cy="48" r="33" fill="#000"/></mask>'
                f'<circle cx="58" cy="64" r="40" fill="{fg}" mask="url(#m)"/>'
                f'<circle cx="94" cy="28" r="7" fill="{accent}"/>')
    if naam == "lateform":
        return (f'<rect x="16" y="16" width="88" height="88" rx="26" fill="none" stroke="{fg}" stroke-width="8"/>'
                f'<path d="M60 60 L37 47" stroke="{fg}" stroke-width="8" stroke-linecap="round"/>'
                f'<path d="M60 60 L60 30" stroke="{accent}" stroke-width="8" stroke-linecap="round"/>'
                f'<circle cx="60" cy="60" r="6" fill="{fg}"/>')
    if naam == "moonform":
        return (f'<circle cx="28" cy="60" r="13" fill="none" stroke="{fg}" stroke-width="5"/>'
                f'<clipPath id="r"><rect x="60" y="0" width="60" height="120"/></clipPath>'
                f'<circle cx="60" cy="60" r="13" fill="none" stroke="{fg}" stroke-width="5"/>'
                f'<circle cx="60" cy="60" r="13" fill="{fg}" clip-path="url(#r)"/>'
                f'<circle cx="92" cy="60" r="15.5" fill="{accent}"/>')
    if naam == "umbralight":
        return (f'<circle cx="66" cy="54" r="40" fill="none" stroke="{accent}" stroke-width="6"/>'
                f'<circle cx="58" cy="62" r="38" fill="{fg if bg == PAPER else bg}" stroke="{fg}" stroke-width="{0 if bg == PAPER else 3}"/>')
    if naam == "pixelbuild":
        # a staircase of pixels being built; the last (accent) pixel drops into place
        cel = lambda k, r: (13 + k * 33, 13 + r * 33)
        vol = [(0, 2), (1, 2), (2, 2), (1, 1), (2, 1)]          # (column, row)
        leeg = [(0, 0), (1, 0), (0, 1)]
        out = "".join(f'<rect x="{cel(k, r)[0]}" y="{cel(k, r)[1]}" width="28" height="28" rx="7" fill="none" '
                      f'stroke="{fg}" stroke-opacity=".25" stroke-width="2"/>' for k, r in leeg)
        out += "".join(f'<rect x="{cel(k, r)[0]}" y="{cel(k, r)[1]}" width="28" height="28" rx="7" fill="{fg}"/>' for k, r in vol)
        x, y = cel(2, 0)
        return out + f'<rect x="{x}" y="{y - 8}" width="28" height="28" rx="7" fill="{accent}"/>'
    raise ValueError(naam)


STIJL = {  # font, size, tracking (em), uppercase
    "pixelbuild": ("InterDisplay-Bold.otf", 64, -0.045, False),
    "duskform": ("InterDisplay-SemiBold.otf", 66, -0.045, False),
    "nachtwerk": ("InterDisplay-Bold.otf", 64, -0.05, False),
    "lateform": ("Inter-Medium.otf", 44, 0.2, True),
    "moonform": ("InterDisplay-Light.otf", 68, -0.025, False),
    "umbralight": ("InterDisplay-Medium.otf", 64, -0.035, False),
}


def logo(naam, thema):
    fg, bg = (PAPER, INK) if thema == "dark" else (INK, PAPER)
    font, grootte, track, hoofd = STIJL[naam]
    d, breedte = tekst_pad(naam.upper() if hoofd else naam, font, grootte, 0, 0, track)
    tekst_x, baseline = 146, 60 + grootte * 0.36
    totaal = tekst_x + breedte + 24
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {totaal:.0f} 120" width="{totaal:.0f}" height="120">'
            f'<rect width="100%" height="100%" fill="{bg}"/>{merk(naam, fg, LIME, bg)}'
            f'<path transform="translate({tekst_x} {baseline:.1f})" d="{d}" fill="{fg}"/></svg>')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for naam in STIJL:
        for thema in ("dark", "light"):
            (OUT / f"{naam}-{thema}.svg").write_text(logo(naam, thema), encoding="utf-8")
        (OUT / f"{naam}-mark.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120">'
            f'<rect width="120" height="120" rx="28" fill="{INK}"/>{merk(naam, PAPER, LIME, INK)}</svg>', encoding="utf-8")
    print(f"{len(STIJL) * 3} logo files written to {OUT}")


if __name__ == "__main__":
    main()
