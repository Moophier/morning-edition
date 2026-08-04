import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

REGISTER_DATA = {"email": "new@test.com", "name": "New User", "password": "secret123"}
LOGIN_DATA = {"email": "new@test.com", "password": "secret123"}


async def test_register_creates_user_and_returns_token(client: AsyncClient):
    response = await client.post("/api/auth/register", json=REGISTER_DATA)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "new@test.com"
    assert data["user"]["name"] == "New User"


async def test_register_rejects_duplicate_email(client: AsyncClient):
    await client.post("/api/auth/register", json=REGISTER_DATA)
    response = await client.post("/api/auth/register", json=REGISTER_DATA)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


async def test_login_with_valid_credentials(client: AsyncClient):
    await client.post("/api/auth/register", json=REGISTER_DATA)
    response = await client.post("/api/auth/login", json=LOGIN_DATA)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "new@test.com"


async def test_login_with_wrong_password_returns_401(client: AsyncClient):
    await client.post("/api/auth/register", json=REGISTER_DATA)
    response = await client.post(
        "/api/auth/login",
        json={"email": "new@test.com", "password": "wrong"},
    )
    assert response.status_code == 401


async def test_me_with_valid_token(client: AsyncClient):
    reg_resp = await client.post("/api/auth/register", json=REGISTER_DATA)
    token = reg_resp.json()["access_token"]
    response = await client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "new@test.com"


async def test_me_without_token_returns_401(client: AsyncClient):
    response = await client.get("/api/auth/me")
    assert response.status_code == 401


async def test_me_with_invalid_token_returns_401(client: AsyncClient):
    response = await client.get(
        "/api/auth/me", headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401
