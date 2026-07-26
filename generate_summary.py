"""
generate_summary.py
--------------------
LAB 4 - GENERATE (uses YOUR OpenAI key).

This calls OpenAI with one fixture's facts and prints an AI match summary.
It is capped at max_summary_runs (default 5).

  python generate_summary.py            # summarise the first fixture, good prompt
  python generate_summary.py --baseline # same fixture, the weak prompt (compare!)
  python generate_summary.py --new # same fixture, the weak prompt (compare!)
  python generate_summary.py --sparse   # the data-poor fixture (watch it hallucinate)

There is ONE blank (#8): the model call itself.
"""

import argparse
import json
from pathlib import Path

from openai import OpenAI

from workshop_utils import load_config, BASE_DIR
from fetch_fixtures import get_fixtures
from prompts import BASELINE_PROMPT, MATCH_REPORT_PROMPT, YOUR_OWN_PROMPT, build_facts_block

RUN_COUNTER = BASE_DIR / "data" / ".summary_runs"
SUMMARY_DIR = BASE_DIR / "data" / "summaries"
SUMMARY_DIR.mkdir(parents=True, exist_ok=True)


def runs_used():
    if RUN_COUNTER.exists():
        return int(RUN_COUNTER.read_text().strip() or "0")
    return 0


def record_run():
    RUN_COUNTER.write_text(str(runs_used() + 1))


def summary_file_path(game_id):
    return SUMMARY_DIR / f"game_{game_id}_summaries.json"


def load_summary_record(game_id):
    path = summary_file_path(game_id)
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_summary_record(game, summary_type, summary_text):
    path = summary_file_path(game["id"])
    record = load_summary_record(game["id"]) or {
        "id": game["id"],
        "home": game["home"],
        "away": game["away"],
        "home_goals": game["home_goals"],
        "away_goals": game["away_goals"],
        "status": game["status"],
        "venue": game["venue"],
        "summaries": {
            "baseline": None,
            "match_report": None,
            "your_own": None,
        },
    }
    record.update({
        "home": game["home"],
        "away": game["away"],
        "home_goals": game["home_goals"],
        "away_goals": game["away_goals"],
        "status": game["status"],
        "venue": game["venue"],
    })
    record["summaries"][summary_type] = summary_text
    with path.open("w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)


def generate(facts, prompt_template, config):
    prompt = prompt_template.format(facts=facts)
    client = OpenAI(api_key=config["openai_key"])

    # ---- FILL IN #8 ----------------------------------------------------
    # Call the chat completions endpoint. Pass the model from config and a
    # single user message containing the prompt. Lower temperature = fewer
    # creative liberties, which is what a newsroom wants.
    response = client.chat.completions.create(
        model=config["openai_model"],
        messages=[{"role": "user", "content": ____}],
        temperature=0.4,
    )
    # --------------------------------------------------------------------

    return response.choices[0].message.content.strip()


def process(use_baseline=False, use_sparse=False, use_new=False):
    config = load_config()

    if runs_used() >= config.get("max_summary_runs", 5):
        print(f"Run limit reached ({config.get('max_summary_runs', 5)}). "
              f"Delete data/.summary_runs to reset for the demo.")
        return

    games = get_fixtures()
    if not games:
        print("No fixtures available to summarize. Check your cache or API settings.")
        return

    # The sparse fixture (no venue/referee) is the last one in the sample.
    game = games[-1] if use_sparse else games[0]

    facts = build_facts_block(game)
    summary_type = "baseline" if use_baseline else "your_own" if use_new else "match_report"
    template = BASELINE_PROMPT if use_baseline else YOUR_OWN_PROMPT if use_new else MATCH_REPORT_PROMPT

    print("=" * 60)
    print(f"FIXTURE: {game['home']} vs {game['away']}")
    prompt_label = 'NEW REPORT (your own)' if use_new else 'BASELINE (weak)' if use_baseline else 'MATCH REPORT (good)'
    print(f"PROMPT:  {prompt_label}")
    print("-" * 60)
    summary_text = generate(facts, template, config)
    print(summary_text)
    print("=" * 60)

    save_summary_record(game, summary_type, summary_text)
    record_run()
    print(f"(runs used: {runs_used()}/{config.get('max_summary_runs', 5)})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", action="store_true", help="use the weak prompt")
    parser.add_argument("--sparse", action="store_true", help="use the data-poor fixture")
    parser.add_argument("--new", action="store_true", help="use the new prompt you wrote in prompts.py")
    args = parser.parse_args()
    process(use_baseline=args.baseline, use_sparse=args.sparse, use_new=args.new)
