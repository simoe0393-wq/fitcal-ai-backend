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

    payload = {
        "message": "hello",
        "calories_goal": 2200,
        "calories_consumed": 1800,
        "protein": 80,
        "protein_target": 150,
        "carbs": 200,
        "carbs_target": 180,
        "fat": 60,
        "fat_target": 70,
        "goal": "lose",
    }
    response2 = client.post(
        "/api/ai-coach/chat",
        json=payload,
        headers={"Authorization": "Bearer mock"},
    )
    assert response2.status_code == 200
    assert "response" in response2.json()

def test_progress_endpoints():
    response = client.post("/api/weight-progress?weight=80.5", headers={"Authorization": "Bearer mock"})
    assert response.status_code == 200
    
    response2 = client.get("/api/water", headers={"Authorization": "Bearer mock"})
    assert response2.status_code == 200

