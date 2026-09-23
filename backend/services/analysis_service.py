from backend.models.toxicity_model import (
    predict_toxicity
)

from backend.models.threat_model import (
    predict_threat
)

from backend.rag.retriever import (
    retrieve
)

from backend.llm.analyzer import (
    explain
)


def analyze_text(text):

    if not text or not text.strip():
        raise ValueError(
            "Text is required."
        )

    toxicity = predict_toxicity(
        text
    )

    threat = predict_threat(
        text
    )

    rag_context = retrieve(
        text
    )

    if (
        threat["threat"]
        and threat["confidence"] >= 0.75
    ):
        risk = "HIGH"

    elif (
        threat["threat"]
        or toxicity["toxic"]
    ):
        risk = "MEDIUM"

    else:
        risk = "LOW"

    explanation = explain(
        text,
        toxicity,
        threat,
        rag_context
    )

    return {
        "text": text,
        "toxicity": toxicity,
        "threat": threat,
        "risk": risk,
        "rag_context": rag_context,
        "explanation": explanation
    }
