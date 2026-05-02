from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_unauthorized_access():
    response = client.get("/api/ai-coach")
    assert response.status_code == 401


def test_analyze_image_endpoint():
    response = client.post("/api/meal/analyze-image", headers={"Authorization": "Bearer mock"})
    # Expect 422 because we didn't send a file, but the endpoint should exist and auth passes
    assert response.status_code == 422

def test_get_barcode_endpoint():
    response = client.get("/api/food/barcode/12345", headers={"Authorization": "Bearer mock"})
    assert response.status_code == 200
    assert response.json()["barcode"] == "12345"

def test_coach_endpoints():
    response = client.get("/api/ai-coach", headers={"Authorization": "Bearer mock"})
    assert response.status_code == 200
    
    response2 = client.post("/api/ai-coach/chat?message=hello", headers={"Authorization": "Bearer mock"})
    assert response2.status_code == 200

def test_progress_endpoints():
    response = client.post("/api/weight-progress?weight=80.5", headers={"Authorization": "Bearer mock"})
    assert response.status_code == 200
    
    response2 = client.get("/api/water", headers={"Authorization": "Bearer mock"})
    assert response2.status_code == 200

