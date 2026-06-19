from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {
        "message": "pong",
    }


def test_create_employee(clean_db):

    payload = {
        "first_name": "Dante",
        "last_name": "Acosta",
        "email": "dante@test.com",
        "position": "Backend Developer",
        "salary": 3000,
        "join_date": "2026-06-19",
    }

    response = client.post(
        "/employees",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == payload["email"]


def test_create_employee_duplicate_email(clean_db):

    payload = {
        "first_name": "Juan",
        "last_name": "Pablo",
        "email": "juampi@test.com",
        "position": "Backend Developer",
        "salary": 3000,
        "join_date": "2026-06-19",
    }

    client.post(
        "/employees",
        json=payload,
    )

    response = client.post(
        "/employees",
        json=payload,
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": "Employee with this email already exists",
    }


def test_get_employee(clean_db):

    payload = {
        "first_name": "Dante",
        "last_name": "Acosta",
        "email": "dante@test.com",
        "position": "Backend Developer",
        "salary": 3000,
        "join_date": "2026-06-19",
    }

    created = client.post(
        "/employees",
        json=payload,
    )

    employee_id = created.json()["id"]

    response = client.get(
        f"/employees/{employee_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == employee_id
    assert data["email"] == payload["email"]


def test_get_employee_not_found(clean_db):

    response = client.get(
        "/employees/999999",
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Employee not found",
    }


def test_update_employee(clean_db):

    payload = {
        "first_name": "Dante",
        "last_name": "Acosta",
        "email": "dante@test.com",
        "position": "Backend Developer",
        "salary": 3000,
        "join_date": "2026-06-19",
    }

    created = client.post(
        "/employees",
        json=payload,
    )

    employee_id = created.json()["id"]

    response = client.put(
        f"/employees/{employee_id}",
        json={
            "salary": 5000,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["salary"] == 5000


def test_update_employee_duplicate_email(clean_db):

    client.post(
        "/employees",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@test.com",
            "position": "Backend",
            "salary": 1000,
            "join_date": "2026-06-19",
        },
    )

    second = client.post(
        "/employees",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@test.com",
            "position": "Backend",
            "salary": 1000,
            "join_date": "2026-06-19",
        },
    )

    employee_id = second.json()["id"]

    response = client.put(
        f"/employees/{employee_id}",
        json={
            "email": "john@test.com",
        },
    )

    assert response.status_code == 409


def test_delete_employee(clean_db):

    created = client.post(
        "/employees",
        json={
            "first_name": "Dante",
            "last_name": "Acosta",
            "email": "dante@test.com",
            "position": "Backend",
            "salary": 3000,
            "join_date": "2026-06-19",
        },
    )

    employee_id = created.json()["id"]

    response = client.delete(
        f"/employees/{employee_id}",
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "Employee deactivated successfully",
    }


def test_average_salary(clean_db):

    client.post(
        "/employees",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@test.com",
            "position": "Backend",
            "salary": 1000,
            "join_date": "2026-06-19",
        },
    )

    client.post(
        "/employees",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@test.com",
            "position": "Backend",
            "salary": 3000,
            "join_date": "2026-06-19",
        },
    )

    response = client.get(
        "/employees/stats/average-salary",
    )

    assert response.status_code == 200

    assert response.json() == {
        "average_salary": 2000.0,
    }