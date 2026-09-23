from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_analyze():
    response = client.post(
        "/api/analyze",
        json={"text": "Your account has been selected. Click the link now."}
    )
    assert response.status_code == 200

    data = response.json()
    assert "toxicity" in data
    assert "threat" in data
    assert "risk" in data
