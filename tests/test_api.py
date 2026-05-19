from fastapi.testclient import TestClient
from Backend.main import app

client = TestClient(app)
def test_prediction():

    payload = {
        "text": "Potato leaf has black spots"
    }

    response = client.post(
        "/predict",
        json=payload
    )

    assert response.status_code == 200