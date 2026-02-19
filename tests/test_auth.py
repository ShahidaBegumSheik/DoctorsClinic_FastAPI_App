import pytest


def test_register_admin_success(client):
    res = client.post("/auth/register", json={"email": "admin1@example.com", "password": "Password123!"})
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == "admin1@example.com"
    assert data["role"] == "ADMIN"


def test_register_duplicate_email_returns_400(client):
    payload = {"email": "dup@example.com", "password": "Password123!"}
    res1 = client.post("/auth/register", json=payload)
    assert res1.status_code == 200

    res2 = client.post("/auth/register", json=payload)
    assert res2.status_code == 400
    assert res2.json()["detail"] == "Email already registered"


def test_register_password_too_short_returns_422(client):
    res = client.post("/auth/register", json={"email": "admin2@example.com", "password": "short"})
    assert res.status_code == 422


def test_login_success_returns_bearer_token(client):
    client.post("/auth/register", json={"email": "admin3@example.com", "password": "Password123!"})

    res = client.post(
        "/auth/login",
        data={"username": "admin3@example.com", "password": "Password123!"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str) and len(data["access_token"]) > 10


def test_login_invalid_credentials_returns_401(client):
    client.post("/auth/register", json={"email": "admin4@example.com", "password": "Password123!"})

    res = client.post(
        "/auth/login",
        data={"username": "admin4@example.com", "password": "WrongPass123!"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert res.status_code == 401
    assert res.json()["detail"] == "Invalid credentials"
