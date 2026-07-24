"""
workshop_utils.py
-----------------
Small shared helpers. This file is GIVEN to you complete — there are no blanks
here. It just loads your config and reads the cached sample data so the rest of
the workshop can stay focused on the interesting parts.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
DATA_DIR = BASE_DIR / "data"


def load_config():
    """Read config.json. If you haven't made it yet, this tells you how."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            "config.json not found. Copy config.example.json to config.json "
            "and paste in your keys."
        )
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_cache(filename):
    """Read one of the bundled sample responses from the data/ folder."""
    path = DATA_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
