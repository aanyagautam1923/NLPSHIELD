from pathlib import Path
import re
import joblib

from backend.nlp.preprocessor import clean_text


ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    ROOT /
    "trained_models" /
    "threat_model.joblib"
)

EXAMPLES_PATH = (
    ROOT /
    "trained_models" /
    "threat_examples.joblib"
)


def word_set(text):
    return set(
        re.findall(
            r"[a-zA-Z0-9]+",
            clean_text(text)
        )
    )


def predict_threat(text: str):

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Threat model not found. "
            "Run: python training/train_threat.py"
        )

    model = joblib.load(
        MODEL_PATH
    )

    cleaned = clean_text(text)

    prediction = int(
        model.predict([cleaned])[0]
    )

    probabilities = model.predict_proba(
        [cleaned]
    )[0]

    confidence = float(
        max(probabilities)
    )

    category = "normal"

    if prediction == 1 and EXAMPLES_PATH.exists():

        examples = joblib.load(
            EXAMPLES_PATH
        )

        query_words = word_set(
            cleaned
        )

        scores = {}

        for category_name, rows in examples.items():

            best_score = 0

            for row in rows:

                row_words = word_set(
                    row
                )

                score = len(
                    query_words &
                    row_words
                )

                best_score = max(
                    best_score,
                    score
                )

            scores[
                category_name
            ] = best_score

        if scores:
            category = max(
                scores,
                key=scores.get
            )

    return {
        "label": prediction,
        "threat": bool(prediction),
        "confidence": round(
            confidence,
            4
        ),
        "category": category
    }
