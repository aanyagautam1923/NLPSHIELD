from backend.nlp.preprocessor import clean_text
from backend.models.model_loader import (
    get_toxicity_model,
    get_threat_model,
    get_threat_examples,
)


def _predict_with_pipeline(model, text: str):
    cleaned = clean_text(text)

    prediction = model.predict([cleaned])[0]

    confidence = 0.0

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba([cleaned])[0]
        confidence = float(max(probabilities))

    return prediction, confidence


def _estimate_category(text: str, threat_examples):
    if not threat_examples:
        return "unknown"

    cleaned = clean_text(text)
    words = set(cleaned.split())

    best_category = "unknown"
    best_score = 0

    for category, examples in threat_examples.items():
        category_score = 0

        for example in examples:
            example_words = set(clean_text(example).split())
            category_score = max(
                category_score,
                len(words.intersection(example_words))
            )

        if category_score > best_score:
            best_score = category_score
            best_category = category

    return best_category


def analyze_text(text: str):
    if not str(text).strip():
        raise ValueError("Text cannot be empty.")

    toxicity_model = get_toxicity_model()
    threat_model = get_threat_model()
    threat_examples = get_threat_examples()

    toxicity_prediction, toxicity_confidence = _predict_with_pipeline(
        toxicity_model,
        text
    )

    threat_prediction, threat_confidence = _predict_with_pipeline(
        threat_model,
        text
    )

    toxic = bool(int(toxicity_prediction))
    threat = bool(int(threat_prediction))

    category = "none"

    if threat:
        category = _estimate_category(
            text,
            threat_examples
        )

    return {
        "toxicity": {
            "label": int(toxicity_prediction),
            "toxic": toxic,
            "confidence": round(toxicity_confidence, 4),
        },
        "threat": {
            "label": int(threat_prediction),
            "threat": threat,
            "confidence": round(threat_confidence, 4),
            "category": category,
        },
    }
