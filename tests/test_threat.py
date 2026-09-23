from backend.models.threat_model import predict_threat


def test_threat_model():
    result = predict_threat(
        "Click this link to verify your bank account password"
    )

    assert "label" in result
    assert "threat" in result
    assert "confidence" in result
    assert "category" in result

    assert isinstance(result["threat"], bool)
    assert 0 <= result["confidence"] <= 1
    assert isinstance(result["category"], str)
