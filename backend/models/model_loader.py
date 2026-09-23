from pathlib import Path
import joblib

from config import (
    TOXICITY_MODEL_PATH,
    THREAT_MODEL_PATH,
    THREAT_EXAMPLES_PATH,
)

_cache = {}


def load_model(path: Path):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Model not found: {path}")

    return joblib.load(path)


def get_toxicity_model():
    if "toxicity" not in _cache:
        _cache["toxicity"] = load_model(TOXICITY_MODEL_PATH)
    return _cache["toxicity"]


def get_threat_model():
    if "threat" not in _cache:
        _cache["threat"] = load_model(THREAT_MODEL_PATH)
    return _cache["threat"]


def get_threat_examples():
    if "threat_examples" not in _cache:
        _cache["threat_examples"] = load_model(THREAT_EXAMPLES_PATH)
    return _cache["threat_examples"]
