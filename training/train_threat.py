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


DATASET = ROOT / "datasets" / "cyber_threat.csv"
MODEL_DIR = ROOT / "trained_models"
MODEL_PATH = MODEL_DIR / "threat_model.joblib"


def train():

    print("=" * 60)
    print("NLPShield - Cyber Threat Model Training")
    print("=" * 60)

    if not DATASET.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET}"
        )

    df = pd.read_csv(DATASET)

    print("\nColumns:", list(df.columns))
    print("Rows:", len(df))

    required = [
        "text",
        "threat",
        "category"
    ]

    for column in required:
        if column not in df.columns:
            raise ValueError(
                f"cyber_threat.csv must contain '{column}'"
            )

    df = df.dropna(
        subset=required
    )

    df["threat"] = pd.to_numeric(
        df["threat"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["threat"]
    )

    df["threat"] = df["threat"].astype(int)

    X = df["text"].apply(clean_text)
    y = df["threat"]

    if y.nunique() < 2:
        raise ValueError(
            "Dataset needs both threat=0 and threat=1."
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

    print("\nTraining cyber-threat model...")

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

    # Save category examples for local category estimation
    category_examples = (
        df[df["threat"] == 1]
        .groupby("category")["text"]
        .apply(list)
        .to_dict()
    )

    joblib.dump(
        category_examples,
        MODEL_DIR / "threat_examples.joblib"
    )

    print("\nModel saved:")
    print(MODEL_PATH)

    print("\nTraining completed successfully.")


if __name__ == "__main__":
    train()
