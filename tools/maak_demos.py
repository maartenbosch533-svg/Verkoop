#!/usr/bin/env python3
"""Genereert per lead een gepersonaliseerde demo-website.

Gebruik:
    python3 tools/maak_demos.py leads/hoveniers_regio_utrecht.csv            # template 'modern'
    python3 tools/maak_demos.py leads/hoveniers_regio_utrecht.csv premium    # template 'premium'

Uitvoer: demos/out/<bedrijf>/index.html  +  demos/out/index.html (overzicht).
Upload de map demos/out gratis naar Netlify Drop (app.netlify.com/drop) of
Cloudflare Pages en stuur een prospect de link naar zijn eigen demo.

Let op: de demo bevat voorbeeldreviews en voorbeeldfoto's. Die zijn alleen
bedoeld om de prospect het ontwerp te laten zien en worden bij een echte
opdracht ALTIJD vervangen door echte reviews en foto's van de klant.
"""
import csv
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULTS = {
    "TELEFOON": "06 - 00 00 00 00",
    "EMAIL": "info@uwbedrijf.nl",
    "JAREN": "10",
    "SCORE": "9,2",
}

BANNER = (
    '<div style="position:relative;z-index:999;background:#111;color:#fff;'
    'font:14px/1.4 system-ui,sans-serif;padding:8px 14px;text-align:center">'
    "Demo-ontwerp voor <b>{naam}</b> &middot; teksten, foto's en reviews zijn voorbeelden"
    "</div>"
)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def regio_van(plaats):
    p = plaats.split("/")[0].strip()
    return f"{p} en omgeving"


def vul_in(template, lead):
    naam = lead["bedrijfsnaam"].strip()
    plaats = lead["plaats"].split("/")[0].strip()
    tel = (lead.get("telefoon") or "").split(";")[0].strip() or DEFAULTS["TELEFOON"]
    email = (lead.get("email") or "").split(";")[0].strip() or DEFAULTS["EMAIL"]
    m = re.search(r"\((\d+[.,]\d)", lead.get("gevonden_via", ""))
    score = m.group(1).replace(".", ",") if m else DEFAULTS["SCORE"]
    tel_cijfers = re.sub(r"\D", "", tel)
    tel_link = "+31" + tel_cijfers[1:] if tel_cijfers.startswith("0") else "+" + tel_cijfers
    waarden = {
        "BEDRIJFSNAAM": naam,
        "PLAATS": plaats,
        "REGIO": regio_van(lead["plaats"]),
        "TELEFOON": tel,
        "TELEFOON_LINK": tel_link,
        "WHATSAPP": tel_link.lstrip("+"),
        "EMAIL": email,
        "JAREN": DEFAULTS["JAREN"],
        "SCORE": score,
    }
    out = template
    for k, v in waarden.items():
        out = out.replace("{{" + k + "}}", html.escape(v))
    return out.replace("<body>", "<body>\n" + BANNER.format(naam=html.escape(naam)), 1)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    soort = sys.argv[2] if len(sys.argv) > 2 else "modern"
    template = (ROOT / "demos" / f"template-{soort}" / "index.html").read_text(encoding="utf-8")
    leads = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
    out_dir = ROOT / "demos" / "out"
    links = []
    for lead in leads:
        s = slug(lead["bedrijfsnaam"])
        d = out_dir / s
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(vul_in(template, lead), encoding="utf-8")
        links.append((lead["bedrijfsnaam"], lead["plaats"], s))
    rijen = "\n".join(
        f'<li><a href="{s}/">{html.escape(n)}</a> <small>{html.escape(p)}</small></li>' for n, p, s in links
    )
    (out_dir / "index.html").write_text(
        '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>Demo-overzicht</title><style>body{font:16px/1.7 system-ui;max-width:700px;margin:40px auto;"
        "padding:0 16px}small{color:#777}</style><h1>Demo's</h1><ol>" + rijen + "</ol>",
        encoding="utf-8",
    )
    print(f"{len(links)} demo's gemaakt in {out_dir}")


if __name__ == "__main__":
    main()
