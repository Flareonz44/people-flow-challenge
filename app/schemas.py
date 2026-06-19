from datetime import date

from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)


class EmployeeCreate(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    position: str = Field(min_length=2, max_length=50)
    salary: float = Field(gt=0)
    join_date: date


class EmployeeResponse(EmployeeCreate):
    id: int
    deactivated: bool

    class Config:
        from_attributes = True


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(default=None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    position: Optional[str] = Field(default=None, min_length=2, max_length=50)
    salary: Optional[float] = Field(default=None, gt=0)
    join_date: Optional[date] = None


class AverageSalaryResponse(BaseModel):
    average_salary: float