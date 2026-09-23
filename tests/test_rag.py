from backend.rag.retriever import retrieve

def test_rag_returns_results():
    results = retrieve("phishing suspicious link password")
    assert isinstance(results, list)
    assert len(results) > 0

def test_rag_result_has_source():
    results = retrieve("phishing")
    assert len(results) > 0
    assert "source" in results[0]
