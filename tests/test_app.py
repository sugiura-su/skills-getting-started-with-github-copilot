import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Math Club"
    # Ensure user is not already signed up
    client.post(f"/activities/{activity}/unregister", params={"email": email})
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    data = response.json()
    assert data["activity"]
    assert email in data["activity"]["participants"]
    # Try signing up again (should fail)
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400

def test_unregister_from_activity():
    email = "testuser2@mergington.edu"
    activity = "Art Club"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup", params={"email": email})
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    data = response.json()
    assert email not in data["activity"]["participants"]
    # Try unregistering again (should fail)
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 400
