from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_analyze_image_endpoint():
    response = client.post("/api/meal/analyze-image", headers={"Authorization": "Bearer mock"})
    # Expect 422 because we didn't send a file, but the endpoint should exist and auth passes
    assert response.status_code == 422

def test_get_barcode_endpoint():
    response = client.get("/api/food/barcode/12345", headers={"Authorization": "Bearer mock"})
    assert response.status_code == 200
    assert response.json()["barcode"] == "12345"
