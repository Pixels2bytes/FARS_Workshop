"""
prompts.py
----------
LAB 4 - VOICE AND TONE.

Two prompts, same data.

  BASELINE_PROMPT  is what a beginner writes: vague, no guardrails.
  MATCH_REPORT_PROMPT  is closer to what FARS actually uses: a role, a voice,
  football-newsroom-journalist conventions, **AND** explicit anti-hallucination rules.
  YOUR_OWN_PROMPT  is where you can experiment with your own prompt-writing skills.

The one rule that matters most for journalism is the last line of the good
prompt: use ONLY the data provided. That single instruction is what keeps the
model from inventing attendance figures, cards. While not fool proof, it is the 
single most important guardrail for factual accuracy.
"""

BASELINE_PROMPT = """Write a summary of this football match in a journalistic style:

{facts}
"""


MATCH_REPORT_PROMPT = """You are a football match reporter for a student newsroom.
Write a tight 120-150 word match report in the style of a wire service (AP/Reuters).

Voice and conventions:
- Lead with the result and the story of the match, not the date.
- Use standard football language.
- Be factual. No predictions, no opinion on quality.
- Refer to teams by name; do not invent nicknames.
- Refer to players on first mention by full name, then by first initial and surname only.
- Note box scores, minute of goals, and cards.

HARD RULE — this is a newsroom, accuracy is everything:
- Use ONLY the facts provided below. If a detail (attendance, venue, scorers, referee,
  cards) is not in the data, DO NOT mention it and DO NOT guess.

MATCH DATA:
{facts}
"""


YOUR_OWN_PROMPT = """ENTER YOUR OWN PROMPT HERE


MATCH DATA:
{facts}
"""


def build_facts_block(game):
    """Turn one normalized fixture dict into a plain-text facts block."""
    return (
        f"Competition: {game.get('league', 'FIFA Club World Cup 2025')}\n"
        f"Home: {game['home']} — {game['home_goals']}\n"
        f"Away: {game['away']} — {game['away_goals']}\n"
        f"Status: {game['status']}\n"
        f"Venue: {game['venue']}"
    )
