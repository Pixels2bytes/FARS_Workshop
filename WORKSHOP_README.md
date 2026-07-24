# FARS Workshop — Build a Sports API Dashboard

**NSEA Workshop · Sports Data Dashboard Edition**
Fetch real football data from api-sports, show it on a live dashboard, then let AI write the match report with a human in the loop.

> **How this repo works.** Several files have blanks marked `# ---- FILL IN #N ----`.
> You fill them in during the session. Every blank has its exact answer in the
> **Answer Key** at the bottom of this file, so if you fall behind you can copy-paste
> and keep moving.

---

## Required Setup (Do NOT Skip)

Please finish all four.

1. **Install Python 3.10+** — check with `python --version`.
2. **Create a free api-sports account** at <https://www.api-sports.io/> → *Free plan available* → sign up → copy your API key from the dashboard. (Free tier = 100 requests/day, plenty for us.)
3. **Create an OpenAI API key** at <https://platform.openai.com/> → API keys → *Create new secret key*.
   - ⚠️ **Unable to Extract OpenAI Key** — If you are unable to create your own key, one will be provided for you throught the google forms sheet provided at the workshop.
4. **Download the FARS Workshop repo** at `github.com/Pixels2bytes/FARS_Workshop`

---

## Install Reqirements

```bash
pip install -r requirements.txt          # flask, requests, openai
cp config.example.json config.json       # then open config.json and paste your two keys
```
**Copy&Paste:** your two keys into `config.json`.

`config.json` is gitignored, so your keys never get committed.

**Safety net:** `config.json` ships with `"use_cache": true`. That means every fetch
reads a bundled sample response from `data/` instead of hitting the network so the
workshop works even if your key isn't ready or the Wi-Fi dies. Flipping `use_cache` to `false` runs against the api.

---

## Lab 1 — Meet the Data

Open `data/fixtures_sample.json`. This is exactly what api-sports sends back for a
`/fixtures` request. Notice the shape:

- Everything real lives inside the top-level **`"response"`** list.
- Each match nests its pieces: `teams.home.name`, `goals.home`, `fixture.status.long`.
- The third match (**Boca Juniors vs Benfica**) is missing its venue and referee.
  Keep an eye on that one. It may sneak its way back in Lab 4.

---

## Lab 2 — Fetch & Normalize Fixtures

Open **`fetch_fixtures.py`**. Fill in blanks **#1–#5**, then run:

```bash
python fetch_fixtures.py
```

Expected example output:

```
[Match Finished] 07-11-25 12:00 PM EST Paris Saint Germain 4-0 Atletico Madrid  @ MetLife Stadium
[Match Finished] 07-14-25 9:00 PM EST Inter 1-1 Monterrey  @ Rose Bowl Stadium
[Match Finished] 07-14-25 12:00 AM EST Boca Juniors 2-2 Benfica  @ Venue TBD
```

What each blank teaches:
- **#1 URL** — every api-sports resource hangs off the base URL.
- **#2 auth header** — the free plan uses the header name `x-apisports-key`.
- **#3 params** — you ask for *one league, one season, one date*.
- **#4 the envelope** — `raw["response"]` is the move you'll use forever.
- **#5 field mapping** — turning nested API fields into flat, dashboard-ready keys.

---

## Lab 3 — Fetch player info *(same pattern, one level deeper)*

Open **`fetch_players.py`**. Player stats are requested by **fixture id**, not by date,
and they nest one level further: team → players → statistics. Fill in **#6–#7**, then run:

```bash
python fetch_players.py
```

Expected output example:

```
O. Dembele (Paris Saint Germain) — 78' rating 8.4, 2 goal(s)
J. Gimenez (Atletico Madrid) — 65' rating 5.4, RED CARD
```

That red card is a **material fact** — exactly the kind of thing a summary must never
miss and never invent. Hold that thought for Lab 4.

---

## Lab 4 — AI summaries + Prompt Voice

We'll run **at most 3 summaries** (the script enforces this) so nobody burns credits.

**Flip the switch first:** set `"use_cache": false` in `config.json` only if you want
live data; the summaries themselves always call OpenAI for real using your key.

Open **`generate_summary.py`**, fill in blank **#8** (the model call), then:

### Run 1 — The Good Prompt
```bash
python generate_summary.py
```
A clean, wire-service-style report of a game.

### Run 2 — The Weak Prompt
```bash
python generate_summary.py --baseline
```
Same match, a vague prompt. Open `prompts.py` and see *why* the good one is better: a **role**, a **voice**, football **conventions and lingo**, and the hard rule section:
*use only the data provided*.


### Run 3 — The Hallucination Trap
```bash
python generate_summary.py --sparse
```
This summarizes the **Boca vs Benfica** fixture. The one with no venue and no
referee. Watch what the model does with the gaps. Does it invent an attendance? The weather? Names its own stadium? **Can you spot the fabrication before you move on?**

> This is the whole point. The model is fluent, confident, and wrong. And it fails
> *silently*. Sparse input data is where hallucinations breed. That's why a
> real newsroom keeps a human-in-the-loop.

---

## Lab 5 — The Dashboard

Open **`app.py`** (blank **#9**) and **`templates/index.html`** (blank **#10**), then:

```bash
python app.py
```

Visit **<http://127.0.0.1:5000>**. Your normalized fixtures render as cards.

> Blank #9 is a teaching point: call `get_fixtures()` *inside* the route, not at
> import time. Otherwise a running server serves stale data and never sees new matches.

---

## Lab 6 — Human-in-the-Loop

This is where the workshop lands. The AI draft is a *starting point*, not a
published article.

- **Why a human must review:** the model can't tell you when it's guessing. A
  journalist checks the score, outcome, and cards against the source data, cuts
  invented details, and owns what publishes.
- **The takeaway:** AI drafts fast; humans make it true. The School of Journalism
  didn't ask us to replace reporters. They asked us to speed up and streamline a newsroom while keeping a journalist accountable for every published word.

---

## Answer Key

**`fetch_fixtures.py`**

```python
# #1
url = f"{config['base_url']}/fixtures"

# #2
headers = {"x-apisports-key": config["api_sports_key"]}

# #3
params = {
    "league": config["league"],
    "season": config["season"],
    "date": config["date"],
}

# #4
matches = raw["response"]

# #5
game = {
    "id": m["fixture"]["id"],
    "home": m["teams"]["home"]["name"],
    "away": m["teams"]["away"]["name"],
    "home_goals": m["goals"]["home"],
    "away_goals": m["goals"]["away"],
    "status": m["fixture"]["status"]["long"],
    "venue": (m["fixture"]["venue"]["name"] or "Venue TBD"),
}
```

**`fetch_players.py`**

```python
# #6
teams = raw["response"]

# #7
stats = entry["statistics"][0]
```

**`generate_summary.py`**

```python
# #8
messages=[{"role": "user", "content": prompt}],
```

**`app.py`**

```python
# #9
games = get_fixtures()
return render_template("index.html", games=games)
```

**`templates/index.html`**

```jinja
<!-- #10 -->
{% for g in games %}
```

---

## For the curious

This is a deliberately small slice of the real system it's based on, **FARS (FIFA
Automated Reporting System)**. FARS holds: manual season-pinned league-ID resolution (api-sports IDs are not stable across seasons), per-fixture status tracking, a full initial →
review → published summary flow, an email pipeline to the newsroom, and a backend handshake with the Makeshift Newsroom for autofill article drafts. FARS will also be expanding to cover other sports.
