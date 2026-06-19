import pytest

from app.database import SessionLocal
from app.models import Employee

@pytest.fixture(autouse=True)
def clean_db():

    db = SessionLocal()

    db.query(Employee).delete()
    db.commit()

    yield

    db.close()