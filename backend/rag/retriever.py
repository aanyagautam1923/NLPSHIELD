from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]

KNOWLEDGE_BASE = (
    ROOT /
    "knowledge_base"
)


def tokenize(text):

    return set(
        re.findall(
            r"[a-zA-Z0-9]+",
            text.lower()
        )
    )


def retrieve(
    query: str,
    top_k: int = 3
):

    query_words = tokenize(
        query
    )

    results = []

    if not KNOWLEDGE_BASE.exists():
        return results

    for file in KNOWLEDGE_BASE.rglob(
        "*.txt"
    ):

        try:
            content = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )
        except Exception:
            continue

        document_words = tokenize(
            content
        )

        score = len(
            query_words &
            document_words
        )

        if score > 0:

            results.append({
                "source": str(
                    file.relative_to(ROOT)
                ),
                "score": score,
                "text": content[:1500]
            })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]
