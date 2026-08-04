import pytest
from httpx import AsyncClient
import pytest_asyncio

pytestmark = pytest.mark.asyncio

REGISTER_DATA = {
    "email": "route@test.com",
    "name": "Route Tester",
    "password": "secret123",
}
OTHER_REGISTER_DATA = {
    "email": "other@test.com",
    "name": "Other User",
    "password": "secret123",
}

ROUTE_CREATE_DATA = {
    "name": "Test Mountain Trail",
    "description": "A beautiful trail through the mountains",
    "difficulty": 2,
    "cost_level": 1,
    "region": "西南",
    "duration_days": "2天",
    "distance_km": 15.5,
    "cumulative_climb": 800,
    "max_elevation": 2500,
    "hero_image": "https://example.com/hero.jpg",
}


@pytest_asyncio.fixture
async def user_token(client: AsyncClient) -> str:
    """Register a user and return their auth token."""
    resp = await client.post("/api/auth/register", json=REGISTER_DATA)
    data = resp.json()
    return data["access_token"]


@pytest_asyncio.fixture
async def other_token(client: AsyncClient) -> str:
    """Register a second user and return their auth token."""
    resp = await client.post("/api/auth/register", json=OTHER_REGISTER_DATA)
    return resp.json()["access_token"]


# --- Tests ---


async def test_list_routes_empty(client: AsyncClient):
    """GET /api/routes returns an empty page when no routes exist."""
    response = await client.get("/api/routes")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["page_size"] == 20


async def test_create_route_requires_auth(client: AsyncClient):
    """POST /api/routes without auth token returns 401."""
    response = await client.post("/api/routes", json=ROUTE_CREATE_DATA)
    assert response.status_code == 401


async def test_create_route_returns_201(client: AsyncClient, user_token: str):
    """POST /api/routes with valid auth returns 201 + route detail."""
    response = await client.post(
        "/api/routes",
        json=ROUTE_CREATE_DATA,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Mountain Trail"
    assert data["slug"] == "test-mountain-trail"
    assert data["difficulty"] == 2
    assert data["region"] == "西南"
    assert "id" in data
    assert "author" in data
    assert data["author"]["name"] == "Route Tester"


async def test_get_route_by_id(client: AsyncClient, user_token: str):
    """GET /api/routes/{id} returns the route."""
    create_resp = await client.post(
        "/api/routes",
        json=ROUTE_CREATE_DATA,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    route_id = create_resp.json()["id"]

    response = await client.get(f"/api/routes/{route_id}")
    assert response.status_code == 200
    assert response.json()["id"] == route_id


async def test_get_route_by_slug(client: AsyncClient, user_token: str):
    """GET /api/routes/slug/{slug} returns the route."""
    create_resp = await client.post(
        "/api/routes",
        json=ROUTE_CREATE_DATA,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    slug = create_resp.json()["slug"]

    response = await client.get(f"/api/routes/slug/{slug}")
    assert response.status_code == 200
    assert response.json()["slug"] == slug


async def test_update_route_by_author(client: AsyncClient, user_token: str):
    """PUT /api/routes/{id} by author succeeds with updated data."""
    create_resp = await client.post(
        "/api/routes",
        json=ROUTE_CREATE_DATA,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    route_id = create_resp.json()["id"]

    update_data = {**ROUTE_CREATE_DATA, "name": "Updated Trail", "difficulty": 3}
    response = await client.put(
        f"/api/routes/{route_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Trail"
    assert data["slug"] == "updated-trail"
    assert data["difficulty"] == 3


async def test_update_route_by_non_author_returns_403(
    client: AsyncClient,
    user_token: str,
    other_token: str,
):
    """PUT /api/routes/{id} by non-author returns 403."""
    create_resp = await client.post(
        "/api/routes",
        json=ROUTE_CREATE_DATA,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    route_id = create_resp.json()["id"]

    response = await client.put(
        f"/api/routes/{route_id}",
        json=ROUTE_CREATE_DATA,
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert response.status_code == 403


async def test_delete_route_by_author(client: AsyncClient, user_token: str):
    """DELETE /api/routes/{id} by author returns 204 and removes the route."""
    create_resp = await client.post(
        "/api/routes",
        json=ROUTE_CREATE_DATA,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    route_id = create_resp.json()["id"]

    response = await client.delete(
        f"/api/routes/{route_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 204

    # Verify it's gone
    get_resp = await client.get(f"/api/routes/{route_id}")
    assert get_resp.status_code == 404


async def test_delete_route_by_non_author_returns_403(
    client: AsyncClient,
    user_token: str,
    other_token: str,
):
    """DELETE /api/routes/{id} by non-author returns 403."""
    create_resp = await client.post(
        "/api/routes",
        json=ROUTE_CREATE_DATA,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    route_id = create_resp.json()["id"]

    response = await client.delete(
        f"/api/routes/{route_id}",
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert response.status_code == 403


async def test_filter_routes_by_difficulty(client: AsyncClient, user_token: str):
    """GET /api/routes?difficulty=N filters by difficulty level."""
    await client.post(
        "/api/routes",
        json={**ROUTE_CREATE_DATA, "name": "Medium Trail", "difficulty": 2},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    await client.post(
        "/api/routes",
        json={**ROUTE_CREATE_DATA, "name": "Expert Trail", "difficulty": 4},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    response = await client.get("/api/routes?difficulty=4")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["name"] == "Expert Trail"


async def test_filter_routes_by_search(client: AsyncClient, user_token: str):
    """GET /api/routes?search=term filters by name/description/region."""
    await client.post(
        "/api/routes",
        json={**ROUTE_CREATE_DATA, "name": "UniqueSearchTerm Trail"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    await client.post(
        "/api/routes",
        json={**ROUTE_CREATE_DATA, "name": "Other Trail"},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    response = await client.get("/api/routes?search=UniqueSearchTerm")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert "UniqueSearchTerm" in data["items"][0]["name"]


async def test_filter_routes_by_cost_level(client: AsyncClient, user_token: str):
    """GET /api/routes?cost_level=N filters by cost level."""
    await client.post(
        "/api/routes",
        json={**ROUTE_CREATE_DATA, "name": "Budget Trail", "cost_level": 1},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    await client.post(
        "/api/routes",
        json={**ROUTE_CREATE_DATA, "name": "Luxury Trail", "cost_level": 3},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    response = await client.get("/api/routes?cost_level=3")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["cost_level"] == 3


async def test_filter_routes_by_region(client: AsyncClient, user_token: str):
    """GET /api/routes?region=X filters by region."""
    await client.post(
        "/api/routes",
        json={**ROUTE_CREATE_DATA, "name": "North Trail", "region": "北方"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    await client.post(
        "/api/routes",
        json={**ROUTE_CREATE_DATA, "name": "South Trail", "region": "南方"},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    response = await client.get("/api/routes?region=北方")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["region"] == "北方"


async def test_get_nonexistent_route_returns_404(client: AsyncClient):
    """GET /api/routes/{nonexistent_id} returns 404."""
    response = await client.get("/api/routes/nonexistent-id")
    assert response.status_code == 404


async def test_get_nonexistent_slug_returns_404(client: AsyncClient):
    """GET /api/routes/slug/{nonexistent_slug} returns 404."""
    response = await client.get("/api/routes/slug/nonexistent-slug")
    assert response.status_code == 404
