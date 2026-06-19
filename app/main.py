from typing import List

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Query,
    status,
)

from sqlalchemy.orm import Session

from app.database import (
    Base,
    engine,
    get_db,
)

from app.models import Employee

from app.schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    AverageSalaryResponse,
)


from app import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="People Flow API", version="1.0.0")


@app.get(
    "/ping",
    tags=["Health"],
    summary="Health check",
    description="Simple endpoint used to verify that the API is running and responsive."
)
def ping():
    return {
        "message": "pong"
    }


@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Employees"],
    summary="Create a new employee",
    description="Creates a new employee and stores it in the database.",
    responses={
        201: {"description": "Employee created successfully"},
        409: {"description": "An employee with the provided email already exists"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"},
    },
)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):

    return crud.create_employee(db, employee)


@app.get(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
    tags=["Employees"],
    summary="Get an employee by ID",
    description="Retrieves a single employee using its unique identifier.",
    responses={
        200: {"description": "Employee retrieved successfully"},
        404: {"description": "Employee not found"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"},
    },
)
def get_employee(employee_id: int, db: Session = Depends(get_db)):

    employee = crud.get_employee(db, employee_id)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return employee


@app.get(
    "/employees",
    response_model=List[EmployeeResponse],
    tags=["Employees"],
    summary="Get employees",
    description="Retrieves a paginated list of employees with optional filtering by position and inclusion of deactivated employees.",
    responses={
        200: {"description": "Employees retrieved successfully"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"},
    },
)
def get_employees(
    position: str | None = Query(
        default=None,
        description="Filter employees by position",
    ),
    include_all: bool = Query(
        default=False,
        description="Include deactivated employees in the results",
    ),
    page: int = Query(
        default=1,
        gt=0,
        description="Page number",
    ),
    page_size: int = Query(
        default=10,
        gt=0,
        le=100,
        description="Number of items per page",
    ),
    db: Session = Depends(get_db),
):

    return crud.get_employees(db, position, include_all, page, page_size)


@app.put(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
    tags=["Employees"],
    summary="Update an employee",
    description="Updates an existing employee using its unique identifier.",
    responses={
        200: {"description": "Employee updated successfully"},
        404: {"description": "Employee not found"},
        409: {"description": "An employee with the provided email already exists"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"},
    },
)
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):

    updated = crud.update_employee(db, employee_id, employee)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return updated


@app.delete(
    "/employees/{employee_id}",
    tags=["Employees"],
    summary="Deactivate an employee",
    description="Marks an employee as deactivated without permanently removing it from the database.",
    responses={
        200: {"description": "Employee deactivated successfully"},
        404: {"description": "Employee not found"},
        500: {"description": "Internal server error"},
    },
)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):

    deleted = crud.delete_employee(db, employee_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return {
        "message": "Employee deactivated successfully",
    }


@app.get(
    "/employees/stats/average-salary",
    response_model=AverageSalaryResponse,
    tags=["Statistics"],
    summary="Get average salary",
    description="Calculates and returns the average salary of all active employees.",
    responses={
        200: {"description": "Average salary calculated successfully"},
        500: {"description": "Internal server error"},
    },
)
def average_salary(db: Session = Depends(get_db)):

    return {
        "average_salary": crud.average_salary(db),
    }
