from fastapi.testclient import TestClient
from Backend.src.main import app

client = TestClient(app)
def test_prediction():

    payload = {
        "text": "Potato leaf has black spots"
    }

    response = client.post(
        "/analyze",
        json=payload
    )

    assert response.status_code == 200