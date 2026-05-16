from app import app17

def test_home():
    client = app17.test_client()

    with client.session_transaction() as sess:
        sess["2fa_passed"] = True

    response = client.get("/")
    assert response.status_code == 200