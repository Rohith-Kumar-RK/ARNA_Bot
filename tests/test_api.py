from fastapi.testclient import TestClient
from Backend.src.main import app

client = TestClient(app)
def test_prediction():
    with open("image.jpg", "rb") as image:
        response = client.post(
            "/analyze",
            files={
                "file": ("image.jpg", image, "image/jpeg")
            }
        )
    # print(response.json())

    assert response.status_code == 200