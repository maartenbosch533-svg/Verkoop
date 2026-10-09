# Verkoop – websites voor hoveniers (vanuit Sofia)

**Model:** Nederlandse hoveniers op afstand een moderne website verkopen.
€750 eenmalig + €75/maand onderhoud. Claude bouwt, jij verkoopt.

**Waarom hoveniers:** één tuinklus levert vaak €3.000–15.000 op, dus een website die één extra klant oplevert, verdient zich direct terug. Veel hoveniers hebben geen of een verouderde site en betalen per lead aan Werkspot of Trustoo.

**Waarom Nederland en niet Sofia:** je spreekt de taal en de prijzen liggen hoger. In Sofia kost een website met een template €400–1.200, in Nederland €500–3.000 bij een freelancer.

## Wat er in deze map staat

| Map / bestand | Wat |
|---|---|
| `leads/hoveniers_regio_utrecht.csv` | 43 hoveniers in de regio Utrecht/Gooi/Vallei. Website en contactgegevens moeten nog worden aangevuld (stap 1). |
| `tools/lead_scanner.py` | Beoordeelt websites, haalt openbare e-mail/telefoon op en zet de beste kansen bovenaan, met **verkooppunten** voor in je gesprek. |
| `tools/maak_demos.py` | Maakt in één keer een **persoonlijke demowebsite per lead** (met hun naam en plaats). |
| `demos/template-modern/` | Demo-ontwerp 1: licht en fris, met offerteformulier (voor de meeste hoveniers). |
| `demos/template-premium/` | Demo-ontwerp 2: luxe uitstraling (voor tuinontwerp en grotere bedrijven). |
| `demos/out/` | 43 kant-en-klare demo's. |
| `outreach/belscript.md` | Belscript met bezwaren en antwoorden. |
| `outreach/emails.md` | Mail- en WhatsApp-teksten. |
| `outreach/offerte.md` | Offertetemplate. |

## Stap voor stap: je eerste week

**Tijd:** Sofia loopt 1 uur voor op Nederland. Jouw 19:00–22:00 is 18:00–21:00 in Nederland.

### Dag 1 (vanavond, 3 uur)
1. **Leads aanvullen (±1,5 uur):** zoek per bedrijf in de CSV op Google Maps naar `[bedrijfsnaam] [plaats]`. Zet website en telefoonnummer in de CSV. Staat er "B.V." achter de naam? Zet dat in `rechtsvorm`. Bedrijven zonder website laat je leeg, dat zijn juist je beste kansen.
2. **Scanner draaien (5 min):** `python3 tools/lead_scanner.py leads/hoveniers_regio_utrecht.csv` geeft je `..._gescand.csv`, gesorteerd op kans.
3. **Demo's opnieuw maken (1 min):** `python3 tools/maak_demos.py leads/hoveniers_regio_utrecht_gescand.csv`. Nu staan de echte telefoonnummers erin.
4. **Online zetten (10 min):** maak een gratis account op [Netlify](https://app.netlify.com/drop) en sleep de map `demos/out` erin. Elke lead heeft dan een eigen link (`.../bedrijfsnaam/`).

### Dag 2–5 (avonden)
- 18:00–19:00 NL-tijd: **10–15 belpogingen** per avond met `belscript.md`.
- Daarna: demo's versturen naar wie "ja" zei en de CSV-status bijwerken.
- Mail de B.V.'s met mail 0 uit `emails.md`.

### Zaterdag (de belangrijkste dag)
- 9:00–12:00 NL (10:00–13:00 Sofia): **bel-blok, 30+ pogingen.** Hoveniers zijn dan vaak bereikbaar.
- Middag: follow-ups en videogesprekken met geïnteresseerden.
- Laat Claude nieuwe leads zoeken in een nieuwe regio, bijvoorbeeld Gelderland of Noord-Brabant.

### Zondag
- Offertes versturen. Na een akkoord bouwt Claude de echte site met de foto's en reviews van de klant.

## De cijfers (realistisch, geen garantie)
Ruwe schatting voor koud bellen met een persoonlijke demo (houd je eigen cijfers bij en stuur bij):
- 100 belpogingen → ±40 bereikt → ±15 willen de demo zien → **±2–4 klanten**
- 2–4 klanten × €750 = **€1.500–3.000** plus €150–300 per maand terugkerend
- Na 3 maanden met 10–15 klanten: ruim **€1.000/maand alleen al aan abonnementen**, plus nieuwe sites.

Het enige wat dit tegenhoudt is te weinig bellen.

## Belangrijk
- **Nooit nep-reviews publiceren.** De demo's bevatten voorbeeldreviews om het ontwerp te tonen. In de echte site komen alleen echte reviews van de klant.
- **E-mailregels:** eenmanszaken en VOF's niet ongevraagd mailen of appen, eerst bellen (Telecommunicatiewet art. 11.7). B.V.'s mag je mailen met een afmeldmogelijkheid.
- **Belasting en registratie:** woon je in Bulgarije, dan registreer je je daar waarschijnlijk als freelancer. Dat is 10% inkomstenbelasting, maar met sociale premies erbij reken je realistisch op ±25%. Op B2B-facturen aan Nederlandse bedrijven geldt btw-verlegging als je btw-geregistreerd bent. **Laat dit checken bij een Bulgaarse boekhouder voordat je de eerste factuur stuurt.**
- **Een Nederlands telefoonnummer** (een VoIP-nummer, een paar euro per maand) verhoogt de kans dat ze opnemen flink. Neem het zodra de eerste klant betaalt.
