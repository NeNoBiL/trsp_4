import pytest
from httpx import AsyncClient, ASGITransport
from faker import Faker

from app.main import app, db

fake = Faker()


@pytest.fixture(autouse=True)
def clear_db():
    db.clear()


@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:

        payload = {
            "username": fake.name(),
            "age": fake.random_int(
                min=18,
                max=60
            )
        }

        response = await client.post(
            "/users",
            json=payload
        )

        assert response.status_code == 201
        assert response.json()["username"] == payload["username"]


@pytest.mark.asyncio
async def test_get_existing_user():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:

        create = await client.post(
            "/users",
            json={
                "username": fake.name(),
                "age": 22
            }
        )

        user_id = create.json()["id"]

        response = await client.get(
            f"/users/{user_id}"
        )

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_non_existing_user():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:

        response = await client.get("/users/999")

        assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:

        create = await client.post(
            "/users",
            json={
                "username": fake.name(),
                "age": 20
            }
        )

        user_id = create.json()["id"]

        response = await client.delete(
            f"/users/{user_id}"
        )

        assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_twice():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:

        create = await client.post(
            "/users",
            json={
                "username": fake.name(),
                "age": 20
            }
        )

        user_id = create.json()["id"]

        await client.delete(f"/users/{user_id}")

        response = await client.delete(
            f"/users/{user_id}"
        )

        assert response.status_code == 404