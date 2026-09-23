from datetime import datetime
from pathlib import Path

from config import REPORTS_DIR


def create_report(result: dict) -> dict:
    toxicity = result.get("toxicity", {})
    threat = result.get("threat", {})

    report = {
        "generated_at": datetime.now().isoformat(
            timespec="seconds"
        ),
        "text": result.get("text", ""),
        "toxicity": {
            "detected": toxicity.get("toxic", False),
            "confidence": toxicity.get("confidence", 0),
        },
        "cyber_threat": {
            "detected": threat.get("threat", False),
            "category": threat.get("category", "none"),
            "confidence": threat.get("confidence", 0),
        },
        "risk": result.get("risk", "LOW"),
        "explanation": result.get("explanation", ""),
    }

    return report


def save_report(report: dict, filename: str = "latest_report.txt"):
    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    path = Path(REPORTS_DIR) / filename

    lines = [
        "NLPShield Security Analysis Report",
        "=" * 40,
        f"Generated: {report.get('generated_at', '')}",
        "",
        f"Text: {report.get('text', '')}",
        "",
        f"Toxicity Detected: "
        f"{report['toxicity']['detected']}",
        f"Toxicity Confidence: "
        f"{report['toxicity']['confidence']}",
        "",
        f"Cyber Threat Detected: "
        f"{report['cyber_threat']['detected']}",
        f"Threat Category: "
        f"{report['cyber_threat']['category']}",
        f"Threat Confidence: "
        f"{report['cyber_threat']['confidence']}",
        "",
        f"Overall Risk: {report.get('risk', 'LOW')}",
        "",
        "Explanation:",
        report.get("explanation", ""),
    ]

    path.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    return path
