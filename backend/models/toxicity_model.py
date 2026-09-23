from pathlib import Path
import joblib

from backend.nlp.preprocessor import clean_text


ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    ROOT /
    "trained_models" /
    "toxicity_model.joblib"
)


def predict_toxicity(text: str):

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Toxicity model not found. "
            "Run: python training/train_toxicity.py"
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

    return {
        "label": prediction,
        "toxic": bool(prediction),
        "confidence": round(
            confidence,
            4
        )
    }
