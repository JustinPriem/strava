"""Baut amsterdam-tour.html aus den Strava-Streams in data/amsterdam/ und src/amsterdam.template.html."""
import json
import math
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Zusammenfassung laut Strava (list_activities)
DAYS = [
    dict(id="18693817681", name="Tag 1", date="2026-05-28", start="2026-05-28T07:42:04", frm="Bad Berka", to="Kassel-Bettenhausen",
         distance=171624, moving=28584, elapsed=40542, elev=1309, effort=365, kcal=6370, cadence=75.1, prs=20),
    dict(id="18781711374", name="Tag 2", date="2026-05-29", start="2026-05-29T08:08:54", frm="Kassel-Bettenhausen", to="Warendorf",
         distance=170158, moving=28860, elapsed=50071, elev=1030, effort=226, kcal=4795, cadence=73.0, prs=12),
    dict(id="18723116349", name="Tag 3", date="2026-05-30", start="2026-05-30T09:25:56", frm="Warendorf", to="Amsterdam",
         distance=265189, moving=44405, elapsed=64793, elev=569, effort=186, kcal=7681, cadence=68.9, prs=13),
]

# Orte, an denen die Route nachweislich vorbeiführt (< 5 km Abstand)
PLACES = [
    ("Bad Berka", 50.899, 11.281, "start"), ("Erfurt", 50.978, 11.029, ""), ("Eisenach", 50.975, 10.320, ""),
    ("Kassel", 51.312, 9.479, "stage"), ("Warburg", 51.490, 9.140, ""), ("Paderborn", 51.718, 8.757, ""),
    ("Rheda-Wiedenbrück", 51.840, 8.300, ""), ("Warendorf", 51.954, 7.989, "stage"), ("Münster", 51.962, 7.626, ""),
    ("Ahaus", 52.076, 7.006, ""), ("Zutphen", 52.140, 6.200, ""), ("Apeldoorn", 52.211, 5.969, ""),
    ("Amersfoort", 52.156, 5.387, "minor"), ("Muiden", 52.330, 5.070, "minor"), ("Amsterdam", 52.373, 4.893, "finish"),
]

PAUSE_MIN_S = 300


def sun_times(day: datetime, lat: float, lon: float):
    """Sonnenauf-/untergang in Ortszeit (MESZ, UTC+2) nach der NOAA-Näherung."""
    n = day.timetuple().tm_yday
    g = 2 * math.pi / 365 * (n - 1)
    eqt = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                    - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    decl = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
            + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    lr = math.radians(lat)
    ha = math.degrees(math.acos(math.cos(math.radians(90.833)) / (math.cos(lr) * math.cos(decl))
                                - math.tan(lr) * math.tan(decl)))
    rise = 720 - 4 * (lon + ha) - eqt + 120
    sset = 720 - 4 * (lon - ha) - eqt + 120
    base = datetime(day.year, day.month, day.day)
    return base + timedelta(minutes=rise), base + timedelta(minutes=sset)


def main():
    out_days = []
    offset_km = 0.0
    for i, meta in enumerate(DAYS, start=1):
        s = json.loads((ROOT / f"data/amsterdam/tag{i}.json").read_text())
        start = datetime.fromisoformat(meta["start"])
        t, loc = s["time"], s["location"]
        pauses = []
        for j in range(len(t) - 1):
            gap = t[j + 1] - t[j]
            if gap >= PAUSE_MIN_S:
                pauses.append(dict(i=j, km=round(s["distance"][j] / 1000, 1), s=gap,
                                   at=(start + timedelta(seconds=t[j])).strftime("%H:%M")))
        lat_mid = sum(p[0] for p in loc) / len(loc)
        lon_mid = sum(p[1] for p in loc) / len(loc)
        rise, sset = sun_times(start, lat_mid, lon_mid)
        out_days.append(dict(
            **{k: meta[k] for k in ("id", "name", "date", "frm", "to", "distance", "moving", "elapsed",
                                     "elev", "effort", "kcal", "cadence", "prs")},
            startSec=start.hour * 3600 + start.minute * 60 + start.second,
            sunset=round((sset - datetime(start.year, start.month, start.day)).total_seconds()),
            sunrise=round((rise - datetime(start.year, start.month, start.day)).total_seconds()) + 86400,
            offsetKm=round(offset_km, 3),
            lat=[round(p[0], 5) for p in loc],
            lon=[round(p[1], 5) for p in loc],
            km=[round(d / 1000, 3) for d in s["distance"]],
            t=t,
            alt=[round(a, 1) for a in s["altitude"]],
            v=[round(v * 3.6, 1) for v in s["velocity_smooth"]],
            hr=[h or 0 for h in s["heart_rate"]],
            pauses=pauses,
        ))
        offset_km += meta["distance"] / 1000

    data = dict(days=out_days, places=[dict(n=n, lat=a, lon=o, kind=k) for n, a, o, k in PLACES])
    tpl = (ROOT / "src/amsterdam.template.html").read_text()
    html = tpl.replace("/*DATA*/", json.dumps(data, separators=(",", ":"), ensure_ascii=False))
    (ROOT / "amsterdam-tour.html").write_text(html)
    for d in out_days:
        print(d["name"], "Pausen:", len(d["pauses"]), "Sonnenuntergang", timedelta(seconds=d["sunset"]),
              "Aufgang", timedelta(seconds=d["sunrise"] - 86400))


if __name__ == "__main__":
    main()
