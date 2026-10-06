# Strava-Trainingsbilanz

- `strava-uebersicht.html` – Übersicht aller Aktivitäten (Dez 2023 bis Sep 2026) mit Tabs für Gesamt, Laufen, Radfahren und Schwimmen: Kennzahlen, Diagramme, Bewertung, Jahresvergleich und Aktivitätslisten.
- `src/uebersicht.template.html` – Vorlage der Seite; `/*DATA*/` wird beim Bauen durch die Aktivitätsdaten ersetzt.
- `data/activities.csv` – Aktivitätsdaten aus Strava (Stand 02.10.2026).
- `amsterdam-tour.html` – Radtour Bad Berka → Amsterdam (28.–31.05.2026): Karte mit Replay, Höhen-/Tempo-/Pulsprofil, Etappen, Pausen und Nachtfahrt. Bauen mit `python3 tools/build_amsterdam.py` aus `src/amsterdam.template.html` und den GPS-Streams in `data/amsterdam/`.
