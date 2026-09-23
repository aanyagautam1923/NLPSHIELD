import json
from typing import Any


def safe_json_dumps(data: Any) -> str:
    return json.dumps(
        data,
        ensure_ascii=False,
        indent=2,
        default=str
    )


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, float(value)))


def normalize_confidence(value: float) -> float:
    return round(clamp(value), 4)
