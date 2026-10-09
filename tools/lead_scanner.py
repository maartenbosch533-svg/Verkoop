#!/usr/bin/env python3
"""Lead scanner: beoordeelt websites van prospects en zet de beste kansen bovenaan.

Gebruik (op je eigen computer, alleen standaard Python 3 nodig):
    python3 tools/lead_scanner.py leads/hoveniers_regio_utrecht.csv

Uitvoer: leads/<naam>_gescand.csv, gesorteerd op kans-score (hoog = beste prospect).
De kolom 'verkooppunten' bevat concrete argumenten voor je belgesprek.

Werkwijze per lead:
  - Geen website ingevuld  -> hoogste score ("geen eigen website").
  - Wel website            -> homepage + /contact ophalen en controleren op
    mobielvriendelijkheid, https, verouderd copyrightjaar, oude techniek,
    ontbrekend offerteformulier, traagheid. E-mail, telefoon en B.V. worden
    automatisch uit de pagina gehaald (alleen openbaar gepubliceerde gegevens).
"""
import csv
import datetime
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (compatible; LeadScanner/1.0)"
THIS_YEAR = datetime.date.today().year
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?:nl|com|eu|be|net|org|info)\b")
PHONE_RE = re.compile(r"(?:\+31|0031|0)\s?(?:6[\s-]?\d{8}|\d{2,3}[\s-]?\d{6,7})")
YEAR_RE = re.compile(r"(?:©|&copy;|copyright)\s*(?:\d{4}\s*[-–]\s*)?(20\d{2})", re.I)
SKIP_EMAIL = ("example.", "uwbedrijf", "sentry", "wixpress", "domain.", "email.", "@2x")


def fetch(url, timeout=15):
    """Return (html, seconds, error)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read(2_000_000)
            charset = resp.headers.get_content_charset() or "utf-8"
            return raw.decode(charset, errors="replace"), time.time() - start, None
    except ssl.SSLError as e:
        return None, time.time() - start, f"ssl: {e}"
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return None, time.time() - start, str(e)


def analyse(url):
    if not url.startswith("http"):
        url = "https://" + url
    score, punten = 0, []

    html, secs, err = fetch(url)
    if html is None and url.startswith("https://"):
        html, secs, err2 = fetch("http://" + url[len("https://"):])
        if html is not None:
            score += 2
            punten.append("geen werkende https (browser toont 'niet veilig')")
    if html is None:
        return 8, ["website onbereikbaar: " + (err or "onbekend")], "", "", ""

    contact_html, _, _ = fetch(url.rstrip("/") + "/contact")
    alle_html = html + (contact_html or "")
    lower = html.lower()

    if 'name="viewport"' not in lower and "name='viewport'" not in lower:
        score += 3
        punten.append("niet mobielvriendelijk (geen viewport) - 60%+ bezoekers zit op mobiel")

    jaren = [int(y) for y in YEAR_RE.findall(html)]
    if jaren and max(jaren) <= THIS_YEAR - 2:
        score += 2
        punten.append(f"copyright {max(jaren)} - site oogt niet onderhouden")

    oud = []
    if re.search(r"jquery[.-]?1\.\d", lower):
        oud.append("jQuery 1.x")
    if "<frameset" in lower or "<frame " in lower:
        oud.append("frames")
    if "<table" in lower and lower.count("<table") >= 3 and "<div" not in lower[:5000]:
        oud.append("tabel-layout")
    if ".swf" in lower:
        oud.append("Flash")
    if oud:
        score += 2
        punten.append("verouderde techniek: " + ", ".join(oud))

    for bouwer in ("jouwweb", "wix.com", "webnode", "mijnwebsite", "site123", "strikingly"):
        if bouwer in lower:
            score += 1
            punten.append(f"gemaakt met {bouwer} (doe-het-zelf uitstraling, advertenties/beperkingen)")
            break

    if "<form" not in alle_html.lower():
        score += 2
        punten.append("geen offerte-/contactformulier - klanten moeten zelf bellen of mailen")
    elif not re.search(r"offerte|afspraak|aanvraag", alle_html, re.I):
        score += 1
        punten.append("geen duidelijke 'offerte aanvragen' knop")

    if not re.search(r"review|beoordeling|recensie|klanten zeggen", lower):
        score += 1
        punten.append("geen reviews op de site (die staan nu alleen op Werkspot/Trustoo)")

    if secs > 3:
        score += 1
        punten.append(f"traag: {secs:.1f}s laadtijd")

    emails = sorted({e for e in EMAIL_RE.findall(alle_html) if not any(s in e.lower() for s in SKIP_EMAIL)})
    phones = sorted({re.sub(r"[\s-]", "", p) for p in PHONE_RE.findall(alle_html)})
    rechtsvorm = "B.V." if re.search(r"\bB\.?V\.?\b", html) else ""

    if not punten:
        punten.append("site lijkt in orde - lage prioriteit (eventueel automatisering aanbieden)")
    return score, punten, "; ".join(emails[:3]), "; ".join(phones[:2]), rechtsvorm


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    rows = list(csv.DictReader(src.open(encoding="utf-8")))
    for i, row in enumerate(rows, 1):
        site = (row.get("website") or "").strip()
        print(f"[{i}/{len(rows)}] {row['bedrijfsnaam']} ...", flush=True)
        if not site:
            row["kans_score"] = 10
            row["verkooppunten"] = ("geen eigen website gevonden - afhankelijk van Werkspot/Trustoo "
                                    "(betaalt per lead, deelt klanten met concurrenten)")
            continue
        score, punten, email, tel, vorm = analyse(site)
        row["kans_score"] = score
        row["verkooppunten"] = " | ".join(punten)
        row["email"] = row.get("email") or email
        row["telefoon"] = row.get("telefoon") or tel
        row["rechtsvorm"] = row.get("rechtsvorm") or vorm

    rows.sort(key=lambda r: int(r["kans_score"]), reverse=True)
    out = src.with_name(src.stem + "_gescand.csv")
    fields = list(rows[0].keys())
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"\nKlaar: {out}  (hoogste score = beste prospect)")


if __name__ == "__main__":
    main()
