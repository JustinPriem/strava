# Strava-Trainingsbilanz

- `strava-uebersicht.html` – Übersicht aller Aktivitäten (Dez 2023 bis Sep 2026) mit Tabs für Gesamt, Laufen, Radfahren und Schwimmen: Kennzahlen, Diagramme, Bewertung, Jahresvergleich und Aktivitätslisten.
- `src/uebersicht.template.html` – Vorlage der Seite; `/*DATA*/` wird beim Bauen durch die Aktivitätsdaten ersetzt.
- `data/activities.csv` – Aktivitätsdaten aus Strava (Stand 02.10.2026).
- `zwiebelmarktlauf-2026.html` – Auswertung des Zwiebelmarktlaufs Weimar (10.10.2026): offizielles Ergebnis, Splits, Strecke, Puls, Segmente, Bestzeiten, Funfacts. Vorlage: `src/zwiebelmarktlauf.template.html`, Verlaufsdaten: `data/zwiebelmarktlauf-2026-race.json`.
