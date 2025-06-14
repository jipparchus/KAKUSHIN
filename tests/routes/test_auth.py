# tests/test_auth.py

def test_register_success(client):
    response = client.post("/auth/register", json={
        "username": "testregister1",
        "password": "Password123?"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_register_duplicate(client):
    # First registration
    client.post("/auth/register", json={
        "username": "testregister2",
        "password": "Password123?"
    })
    # Try again
    response = client.post("/auth/register", json={
        "username": "testregister2",
        "password": "Password123?"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username exists"


def test_login_success(client):
    client.post("/auth/register", json={
        "username": "testlogin1",
        "password": "Password123?"
    })
    response = client.post("/auth/login", json={
        "username": "testlogin1",
        "password": "Password123?"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "username": "testwlogin2",
        "password": "Password123?"
    })
    response = client.post("/auth/login", json={
        "username": "testwlogin2",
        "password": "Password123!"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
