from app import app17

def test_home():
    client = app17.test_client()
    response = client.get("/")
    assert response.status_code == 200