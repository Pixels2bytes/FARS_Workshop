"""
app.py
------
LAB 5 - THE DASHBOARD.

A tiny Flask app that renders your fixtures in the browser. This is the payoff:
the JSON you wrangled in Labs 2-3 shows up as a real web page.

One blank (#9): the route that hands your fixtures to the template.

Run it:   python app.py     then open  http://127.0.0.1:5000 in a browser.
"""

import json
from pathlib import Path

from flask import Flask, render_template

from fetch_fixtures import get_fixtures
from workshop_utils import BASE_DIR

app = Flask(__name__)
SUMMARY_DIR = BASE_DIR / "data" / "summaries"
SUMMARY_DIR.mkdir(parents=True, exist_ok=True)


def load_summary_record(game_id):
    path = SUMMARY_DIR / f"game_{game_id}_summaries.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"summaries": {"baseline": None, "match_report": None, "your_own": None}}


@app.route("/")
def dashboard():
    # ---- FILL IN #9 ----------------------------------------------------
    # 1) call get_fixtures() to load the (normalized) match list
    # 2) render index.html, passing that list in as "games"
    #
    # IMPORTANT: call get_fixtures() *inside* the route, not at import time,
    # so every page refresh re-reads the latest data instead of a stale copy.
    games = ______
    for game in games:
        record = load_summary_record(game["id"])
        game["summaries"] = record.get("summaries", {"baseline": None, "match_report": None, "your_own": None})
    return render_template("index.html", games=_____)
    # --------------------------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True, port=5000)
