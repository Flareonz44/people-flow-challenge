from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    Boolean,
)

from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False, index=True)

    position = Column(String, nullable=False)

    salary = Column(Float, nullable=False)

    deactivated = Column(Boolean, nullable=False, default=False)

    join_date = Column(Date, nullable=False)
