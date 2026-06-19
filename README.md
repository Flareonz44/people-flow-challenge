# PeopleFlow - Employee Management API

REST API for employee management built with FastAPI, PostgreSQL, Docker and SQLAlchemy.

## Features

- Create employees
- List employees
- Filter employees by position
- Pagination support
- Get employee by ID
- Update employees
- Soft delete employees
- Average salary statistics
- OpenAPI / Swagger documentation
- Pytest test suite
- Dockerized environment

---

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Pytest
- Docker & Docker Compose

---

## API Documentation

Once the application is running:

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

## Running with Docker

### Build and start the application

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

### Stop containers

```bash
docker compose down
```

### Stop containers and remove volumes

```bash
docker compose down -v
```

---

## Running Locally

### Create virtual environment

```bash
python -m venv .venv
```

### Activate environment

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure PostgreSQL

Create a PostgreSQL database:

```sql
CREATE DATABASE people_flow_db;
```

Configure the database connection through the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/people_flow_db
```

### Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

---

## Running Tests

Run the full test suite:

```bash
pytest
```

Verbose output:

```bash
pytest -v
```

---

## Employee Model

Each employee contains:

| Field | Type |
|---------|---------|
| id | integer |
| first_name | string |
| last_name | string |
| email | string |
| position | string |
| salary | float |
| join_date | date |

---

## Available Endpoints

### Health

| Method | Endpoint |
|----------|----------|
| GET | /health |

### Employees

| Method | Endpoint |
|----------|----------|
| POST | /employees |
| GET | /employees |
| GET | /employees/{employee_id} |
| PUT | /employees/{employee_id} |
| DELETE | /employees/{employee_id} |

### Statistics

| Method | Endpoint |
|----------|----------|
| GET | /employees/stats/average-salary |

---

## Bonus Features Implemented

- Swagger / OpenAPI documentation
- Docker support
- Automated tests with Pytest
- Soft delete implementation
- Input validation with Pydantic
- Employee filtering and pagination

---

## Author

Technical challenge developed for Leafnoise for a Backend Developer position by Dante Acosta.