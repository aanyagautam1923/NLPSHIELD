from pathlib import Path
from typing import List, Dict

from config import KNOWLEDGE_BASE_DIR


def load_documents(directory=None) -> List[Dict[str, str]]:
    base_dir = Path(directory) if directory else Path(KNOWLEDGE_BASE_DIR)

    documents = []

    if not base_dir.exists():
        return documents

    for path in base_dir.rglob("*.txt"):
        try:
            text = path.read_text(encoding="utf-8-sig").strip()
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="replace").strip()

        if not text:
            continue

        documents.append({
            "source": str(path.relative_to(base_dir)),
            "text": text,
        })

    return documents


def load_document(path) -> Dict[str, str]:
    path = Path(path)

    text = path.read_text(
        encoding="utf-8-sig",
        errors="replace"
    ).strip()

    return {
        "source": str(path),
        "text": text,
    }
