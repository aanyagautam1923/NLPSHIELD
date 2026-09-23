from pathlib import Path
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

from backend.nlp.preprocessor import clean_text


ROOT = Path(__file__).resolve().parents[1]


def evaluate_toxicity():

    path = ROOT / "datasets" / "toxicity.csv"

    df = pd.read_csv(path)

    df["clean_text"] = df["text"].apply(clean_text)

    X_train, X_test, y_train, y_test = train_test_split(
        df["clean_text"],
        df["label"],
        test_size=0.2,
        random_state=42,
        stratify=df["label"]
    )

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=1
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    )

    model.fit(X_train_vec, y_train)

    predictions = model.predict(X_test_vec)

    print("\n==============================")
    print("NLPShield Toxicity Evaluation")
    print("==============================")

    print(
        f"Accuracy : {accuracy_score(y_test, predictions):.4f}"
    )

    print(
        f"Precision: {precision_score(y_test, predictions, zero_division=0):.4f}"
    )

    print(
        f"Recall   : {recall_score(y_test, predictions, zero_division=0):.4f}"
    )

    print(
        f"F1 Score : {f1_score(y_test, predictions, zero_division=0):.4f}"
    )

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )


def evaluate_threat():

    path = ROOT / "datasets" / "cyber_threat.csv"

    df = pd.read_csv(path)

    df["clean_text"] = df["text"].apply(clean_text)

    X_train, X_test, y_train, y_test = train_test_split(
        df["clean_text"],
        df["threat"],
        test_size=0.2,
        random_state=42,
        stratify=df["threat"]
    )

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=1
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    )

    model.fit(X_train_vec, y_train)

    predictions = model.predict(X_test_vec)

    print("\n==============================")
    print("NLPShield Threat Evaluation")
    print("==============================")

    print(
        f"Accuracy : {accuracy_score(y_test, predictions):.4f}"
    )

    print(
        f"Precision: {precision_score(y_test, predictions, zero_division=0):.4f}"
    )

    print(
        f"Recall   : {recall_score(y_test, predictions, zero_division=0):.4f}"
    )

    print(
        f"F1 Score : {f1_score(y_test, predictions, zero_division=0):.4f}"
    )

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )


if __name__ == "__main__":

    evaluate_toxicity()
    evaluate_threat()
