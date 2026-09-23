from backend.models.toxicity_model import predict_toxicity


def test_toxicity_model():
    result = predict_toxicity("I hate you")

    assert "label" in result
    assert "toxic" in result
    assert "confidence" in result

    assert isinstance(result["toxic"], bool)
    assert 0 <= result["confidence"] <= 1
