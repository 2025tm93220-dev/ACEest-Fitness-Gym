import pytest

from app import create_app


@pytest.fixture()
def client(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "test.db"),
            "ADMIN_PASSWORD": "test-password",
        }
    )

    with app.test_client() as test_client:
        yield test_client


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_login_accepts_configured_admin(client):
    response = client.post(
        "/login",
        json={
            "username": "admin",
            "password": "test-password",
        },
    )

    assert response.status_code == 200
    assert response.get_json()["role"] == "Admin"


def test_client_creation_and_duplicate_protection(client):
    payload = {
        "name": "Asha",
        "program": "Fat Loss",
    }

    created = client.post("/clients", json=payload)
    duplicate = client.post("/clients", json=payload)

    assert created.status_code == 201
    assert duplicate.status_code == 409


def test_workout_creation_and_listing(client):
    client_response = client.post(
        "/clients",
        json={"name": "Ravi"},
    )

    client_id = client_response.get_json()["id"]

    workout = client.post(
        f"/clients/{client_id}/workouts",
        json={
            "date": "2026-09-29",
            "workout_type": "Strength",
            "duration_min": 60,
            "notes": "Upper body",
        },
    )

    workouts = client.get(
        f"/clients/{client_id}/workouts"
    )

    assert workout.status_code == 201
    assert len(workouts.get_json()) == 1
    assert workouts.get_json()[0]["workout_type"] == "Strength"
