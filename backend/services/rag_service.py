from backend.rag.knowledge_base import knowledge_base


def retrieve_security_context(
    query: str,
    top_k: int = 5
):
    if not query or not query.strip():
        return []

    return knowledge_base.search(
        query.strip(),
        top_k=top_k
    )


def get_security_guidance(query: str):
    results = retrieve_security_context(
        query,
        top_k=5
    )

    guidance = []

    for item in results:
        guidance.append({
            "source": item["source"],
            "score": item["score"],
            "text": item["text"]
        })

    return guidance
