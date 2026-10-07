import json
from pathlib import Path

DATA_DIR = Path("data")
HISTORY_FILE = DATA_DIR / "history.json"


def _ensure():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text("[]", encoding="utf-8")


def load_history():
    _ensure()

    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def add_observation(item):
    history = load_history()
    history.insert(0, item)

    HISTORY_FILE.write_text(
        json.dumps(history[:100], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
