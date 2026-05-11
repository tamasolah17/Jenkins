from Jenkins import app17

def test_login_route():
    client = app17.test_client()

    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'pass@123'
    })

    assert response.status_code == 200