import pytest

def test_register_user(client):
    response = client.post(
        "/register",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_register_user_duplicate_email(client):
    client.post(
        "/register",
        json={"email": "test@example.com", "password": "password123"},
    )
    response = client.post(
        "/register",
        json={"email": "test@example.com", "password": "password456"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_user(client):
    client.post(
        "/register",
        json={"email": "test@example.com", "password": "password123"},
    )
    response = client.post(
        "/token",
        data={"username": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_user_invalid_credentials(client):
    client.post(
        "/register",
        json={"email": "test@example.com", "password": "password123"},
    )
    response = client.post(
        "/token",
        data={"username": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"
