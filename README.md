# FARS Workshop — Sports API Dashboard

A hands-on, fill-in-the-blank workshop: pull real football data from
[api-sports](https://www.api-sports.io/), display it on a live Flask dashboard, and
generate AI match summaries with a human editor in the loop.

### Start here: [`WORKSHOP_README.md`](WORKSHOP_README.md)

That file has the pre-work, every step, and a copy-paste answer key.

### Quick start
```bash
python -m venv venv                  # WINDOWS LINE: create virtual environment
venv/scripts/activate​                # "                                       "

python3 -m venv venv​                 # Mac / Unix / Linux: ​create virtual environment
source venv/bin/activate​             # "                                             "

pip install -r requirements.txt
cp config.example.json config.json   # paste your api-sports + OpenAI keys
python fetch_fixtures.py             # works offline thanks to cached sample data
python app.py                        # dashboard at http://127.0.0.1:5000
```

### What's in here
| File | Role |
|------|------|
| `workshop_readme.md` | The workshop itself — read this |
| `fetch_fixtures.py` | Fetch + normalize matches (fill-in) |
| `fetch_players.py` | Fetch player stats for a fixture (fill-in) |
| `prompts.py` | Baseline vs journalistic prompt |
| `generate_summary.py` | AI summary, capped at 5 runs (fill-in) |
| `app.py` / `templates/` / `static/` | The Flask dashboard (fill-in) |
| `data/*_sample.json` | Cached API responses as the offline safety net |

Based on **FARS (FIFA Automated Reporting System)**.
