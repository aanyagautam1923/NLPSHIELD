from pathlib import Path
import sys
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report
)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.nlp.preprocessor import clean_text


DATASET = ROOT / "datasets" / "toxicity.csv"
MODEL_DIR = ROOT / "trained_models"
MODEL_PATH = MODEL_DIR / "toxicity_model.joblib"


def train():

    print("=" * 60)
    print("NLPShield - Toxicity Model Training")
    print("=" * 60)

    if not DATASET.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET}"
        )

    df = pd.read_csv(DATASET)

    print("\nColumns:", list(df.columns))
    print("Rows:", len(df))

    if "text" not in df.columns:
        raise ValueError(
            "toxicity.csv must contain a 'text' column"
        )

    if "label" not in df.columns:
        raise ValueError(
            "toxicity.csv must contain a 'label' column"
        )

    df = df.dropna(
        subset=["text", "label"]
    )

    df["label"] = pd.to_numeric(
        df["label"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["label"]
    )

    df["label"] = df["label"].astype(int)

    X = df["text"].apply(clean_text)
    y = df["label"]

    if y.nunique() < 2:
        raise ValueError(
            "Dataset needs at least two labels."
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                ngram_range=(1, 2),
                min_df=1,
                sublinear_tf=True
            )
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced"
            )
        )
    ])

    print("\nTraining model...")

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print("\nAccuracy:", round(accuracy, 4))

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    MODEL_DIR.mkdir(
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_PATH
    )

    print("\nModel saved:")
    print(MODEL_PATH)

    print("\nTraining completed successfully.")


if __name__ == "__main__":
    train()
