from backend.rag.document_loader import load_documents
from backend.rag.embeddings import LocalEmbeddingStore


class KnowledgeBase:
    def __init__(self):
        self.documents = []
        self.store = LocalEmbeddingStore()
        self.loaded = False

    def load(self):
        self.documents = load_documents()
        self.store.fit(self.documents)
        self.loaded = True
        return len(self.documents)

    def search(self, query: str, top_k: int = 5):
        if not self.loaded:
            self.load()

        return self.store.search(
            query,
            top_k=top_k
        )


knowledge_base = KnowledgeBase()
