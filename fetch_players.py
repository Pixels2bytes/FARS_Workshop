"""
fetch_players.py
----------------
LAB 3 - SAME PATTERN, ONE LEVEL DEEPER.

Fixtures gave you the match. Now we ask api-sports who played and how they did,
for a single fixture. The shape is the same idea as fetch_fixtures.py (an
envelope with a "response" list) but nested one level further: each team holds
a list of players, and each player holds a list of statistics.

Only two blanks here — you already know the moves from Lab 2.

Run it on its own to test:   python fetch_players.py
"""

import requests
import json

from workshop_utils import load_config, load_cache, BASE_DIR

PLAYERS_DIR = BASE_DIR / "data" / "players"
PLAYERS_DIR.mkdir(parents=True, exist_ok=True)


def fetch_raw_players(config, fixture_id):
    if config.get("use_cache"):
        return load_cache("players_sample.json")

    url = f"{config['base_url']}/fixtures/players"
    headers = {"x-apisports-key": config["api_sports_key"]}
    # NOTE: player stats are requested by fixture id, not by date.
    params = {"fixture": fixture_id}

    response = requests.get(url, headers=headers, params=params, timeout=15)
    response.raise_for_status()
    
    # Save players data to JSON file
    players_json_path = PLAYERS_DIR / f"players_{fixture_id}.json"
    with open(players_json_path, "w", encoding="utf-8") as f:
        json.dump(response.json(), f, indent=2)

    return response.json()


def normalize_players(raw):
    """Flatten to one row per player with the stats a journalist actually uses."""
    # ---- FILL IN #6 ----------------------------------------------------
    # Same envelope move as before: the teams live under "response".
    teams = raw[____]
    # --------------------------------------------------------------------

    players = []
    for team in teams:
        team_name = team["team"]["name"]
        for entry in team["players"]:
            # ---- FILL IN #7 --------------------------------------------
            # Each player's numbers live in statistics[0] (a one-item list).
            # Grab that first stat block.
            stats = entry["statistics"][____]
            # ------------------------------------------------------------
            players.append({
                "team": team_name,
                "name": entry["player"]["name"],
                "minutes": stats["games"]["minutes"],
                "rating": stats["games"]["rating"],
                "goals": stats["goals"]["total"] or 0,
                "assists": stats["goals"]["assists"] or 0,
                "yellow": stats["cards"]["yellow"],
                "red": stats["cards"]["red"],
            })

    return players


def get_players(fixture_id):
    config = load_config()
    raw = fetch_raw_players(config, fixture_id)
    return normalize_players(raw)


if __name__ == "__main__":
    for p in get_players(1141650):
        line = f"{p['name']} ({p['team']}) — {p['minutes']}' rating {p['rating']}"
        if p["goals"]:
            line += f", {p['goals']} goal(s)"
        if p["red"]:
            line += ", RED CARD"
        print(line)
