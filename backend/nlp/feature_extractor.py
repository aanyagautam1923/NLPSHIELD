from sklearn.feature_extraction.text import TfidfVectorizer

from backend.nlp.preprocessor import clean_text


class TextFeatureExtractor:
    def __init__(self, ngram_range=(1, 2)):
        self.vectorizer = TfidfVectorizer(
            ngram_range=ngram_range,
            min_df=1
        )
        self.is_fitted = False

    def fit(self, texts):
        cleaned = [clean_text(text) for text in texts]
        self.vectorizer.fit(cleaned)
        self.is_fitted = True
        return self

    def transform(self, texts):
        if not self.is_fitted:
            raise RuntimeError(
                "Feature extractor must be fitted before transform()."
            )

        cleaned = [clean_text(text) for text in texts]
        return self.vectorizer.transform(cleaned)

    def fit_transform(self, texts):
        cleaned = [clean_text(text) for text in texts]
        result = self.vectorizer.fit_transform(cleaned)
        self.is_fitted = True
        return result
