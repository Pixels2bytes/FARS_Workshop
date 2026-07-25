"""
fetch_fixtures.py
-----------------
LAB 2 - THE MAIN EVENT

This is where you "complete the circuit": ask api-sports for a list of matches
(fixtures) and turn its big messy JSON into a small clean list your dashboard
can render.

Look for the  # ---- FILL IN #N ----  markers. Each one has a matching answer
in workshop_readme.md, so if you fall behind you can copy-paste and keep going.

Run it on its own to test:   python fetch_fixtures.py
"""

import requests
from datetime import datetime, timedelta, timezone

from workshop_utils import load_config, load_cache


def fetch_raw_fixtures(config):
    """
    Ask api-sports for the fixtures. If use_cache is on (or a request fails),
    fall back to the bundled sample so the workshop never gets stuck.
    """
    if config.get("use_cache"):
        return load_cache("fixtures_sample.json")

    # ---- FILL IN #1 ----------------------------------------------------
    # The endpoint. api-sports serves fixtures at  <base_url>/fixtures
    # Build the full URL from config["base_url"].
    url = ____
    # --------------------------------------------------------------------

    # ---- FILL IN #2 ----------------------------------------------------
    # The auth header. On the free api-sports.io plan the header name is
    # exactly  x-apisports-key  and its value is your key.
    headers = {____: config["api_sports_key"]}
    # --------------------------------------------------------------------

    # ---- FILL IN #3 ----------------------------------------------------
    # The query params. We want one league, one season, and one date.
    # The config keys are already there for you: "league", "season", "date".
    params = {
        "league": config[____],
        "season": config[____],
        "date": config[____],
    }
    # --------------------------------------------------------------------

    response = requests.get(url, headers=headers, params=params, timeout=15)
    response.raise_for_status()
    return response.json()


def normalize_fixtures(raw):
    """
    Turn the raw api-sports payload into a flat list of simple dicts.

    KEY IDEA: api-sports wraps everything in a "response" list. Every real
    match lives inside there. Reaching into it is the single most important
    move when working with this API.
    """
    # ---- FILL IN #4 ----------------------------------------------------
    # Pull the list of matches out of the envelope. It lives under the
    # top-level "response" key.
    matches = raw[____]
    # --------------------------------------------------------------------

    def to_est_label(iso_datetime):
        dt = datetime.fromisoformat(iso_datetime)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        est = dt.astimezone(timezone(timedelta(hours=-5)))
        return est.strftime("%m-%d-%y %I:%M %p EST")

    games = []
    for m in matches:
        # ---- FILL IN #5 ------------------------------------------------
        # Map the nested api-sports fields onto flat, dashboard-friendly keys.
        # Follow the dotted paths in the JSON:
        #   teams.home.name / teams.away.name / goals.home / goals.away
        #   fixture.status.long / fixture.id
        game = {
            "id": m["fixture"]["id"],
            "home": m["teams"]["home"][____],
            "away": m["teams"]["away"][____],
            "home_goals": m["goals"][____],
            "away_goals": m["goals"][____],
            "status": m["fixture"]["status"]["long"],
            "venue": (m["fixture"]["venue"]["name"] or "Venue TBD"),
            "date_time_est": to_est_label(m["fixture"]["date"]),
        }
        # ----------------------------------------------------------------
        games.append(game)

    return games


def get_fixtures():
    """Public entry point the dashboard calls."""
    config = load_config()
    raw = fetch_raw_fixtures(config)
    return normalize_fixtures(raw)


if __name__ == "__main__":
    for g in get_fixtures():
        print(f"[{g['status']}] {g['home']} {g['home_goals']}-{g['away_goals']} {g['away']}  @ {g['venue']}")
