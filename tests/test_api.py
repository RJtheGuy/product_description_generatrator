import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Product Description Generator API" in response.json()["message"]

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_generate_description():
    request_data = {
        "product_name": "Test Product",
        "raw_text": "This is a great product with amazing features",
        "category": "Electronics",
        "target_length": 100
    }
    
    response = client.post("/api/v1/generate-description", json=request_data)
    # Note: This test will fail without Ollama running
    # In real tests, you'd mock the Ollama client
