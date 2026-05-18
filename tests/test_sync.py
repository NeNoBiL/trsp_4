from fastapi.testclient import TestClient
from app.main import app, db

client = TestClient(app)


def setup_function():
    db.clear()


def test_create_user():
    response = client.post(
        "/users",
        json={
            "username": "Alex",
            "age": 20
        }
    )

    assert response.status_code == 201
    assert response.json()["username"] == "Alex"


def test_get_user():
    create = client.post(
        "/users",
        json={
            "username": "Ivan",
            "age": 25
        }
    )

    user_id = create.json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200


def test_delete_user():
    create = client.post(
        "/users",
        json={
            "username": "Kate",
            "age": 30
        }
    )

    user_id = create.json()["id"]

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 204