from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer


class LocalEmbeddingStore:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
        self.documents = []
        self.matrix = None

    def fit(self, documents: List[dict]):
        self.documents = documents

        texts = [
            item["text"]
            for item in documents
        ]

        if not texts:
            self.matrix = None
            return self

        self.matrix = self.vectorizer.fit_transform(texts)
        return self

    def search(self, query: str, top_k: int = 5):
        if self.matrix is None or not self.documents:
            return []

        query_vector = self.vectorizer.transform([query])

        scores = (
            self.matrix @ query_vector.T
        ).toarray().ravel()

        ranked = scores.argsort()[::-1]

        results = []

        for index in ranked[:top_k]:
            score = float(scores[index])

            if score <= 0:
                continue

            results.append({
                "source": self.documents[index]["source"],
                "score": round(score, 4),
                "text": self.documents[index]["text"]
            })

        return results
