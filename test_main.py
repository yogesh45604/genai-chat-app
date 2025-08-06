from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_session():
    response = client.post("/sessions", json={"session_user": "  Alice  "})
    assert response.status_code == 200
    data = response.json()
    assert data["session_user"] == "alice"

def test_create_session_empty_user():
    response = client.post("/sessions", json={"session_user": "   "})
    assert response.status_code == 400

def test_add_message():
    response = client.post("/sessions/1/messages", json={"role": "user", "content": "What is AI?"})
    assert response.status_code == 200

def test_add_message_invalid_session():
    response = client.post("/sessions/999/messages", json={"role": "user", "content": "Test"})
    assert response.status_code == 404

def test_get_messages():
    response = client.get("/sessions/1/messages")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_messages_with_filter():
    response = client.get("/sessions/1/messages?role=user")
    assert response.status_code == 200
    messages = response.json()
    assert all(msg["role"] == "user" for msg in messages)
