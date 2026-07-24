"""
generate_summary.py
--------------------
LAB 4 - GENERATE (uses YOUR OpenAI key).

This calls OpenAI with one fixture's facts and prints an AI match summary.
It is capped at max_summary_runs (default 3) so nobody burns through credits.

  python generate_summary.py            # summarise the first fixture, good prompt
  python generate_summary.py --baseline # same fixture, the weak prompt (compare!)
  python generate_summary.py --sparse   # the data-poor fixture (watch it hallucinate)

There is ONE blank (#8): the model call itself.
"""

import argparse
from pathlib import Path

from openai import OpenAI

from workshop_utils import load_config, BASE_DIR
from fetch_fixtures import get_fixtures
from prompts import BASELINE_PROMPT, MATCH_REPORT_PROMPT, build_facts_block

RUN_COUNTER = BASE_DIR / "data" / ".summary_runs"


def runs_used():
    if RUN_COUNTER.exists():
        return int(RUN_COUNTER.read_text().strip() or "0")
    return 0


def record_run():
    RUN_COUNTER.write_text(str(runs_used() + 1))


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


def process(use_baseline=False, use_sparse=False):
    config = load_config()

    if runs_used() >= config.get("max_summary_runs", 3):
        print(f"Run limit reached ({config.get('max_summary_runs', 3)}). "
              f"Delete data/.summary_runs to reset for the demo.")
        return

    games = get_fixtures()
    # The sparse fixture (no venue/referee) is the last one in the sample.
    game = games[-1] if use_sparse else games[0]

    facts = build_facts_block(game)
    template = BASELINE_PROMPT if use_baseline else MATCH_REPORT_PROMPT

    print("=" * 60)
    print(f"FIXTURE: {game['home']} vs {game['away']}")
    print(f"PROMPT:  {'BASELINE (weak)' if use_baseline else 'MATCH REPORT (good)'}")
    print("-" * 60)
    print(generate(facts, template, config))
    print("=" * 60)

    record_run()
    print(f"(runs used: {runs_used()}/{config.get('max_summary_runs', 3)})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", action="store_true", help="use the weak prompt")
    parser.add_argument("--sparse", action="store_true", help="use the data-poor fixture")
    args = parser.parse_args()
    process(use_baseline=args.baseline, use_sparse=args.sparse)
