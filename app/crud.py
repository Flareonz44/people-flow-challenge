from sqlalchemy import func

from fastapi import HTTPException, status

from app.models import Employee
from app.schemas import EmployeeCreate
from app.schemas import EmployeeUpdate


def create_employee(db, employee: EmployeeCreate):

    existing_employee = (
        db.query(Employee)
        .filter(Employee.email == employee.email)
        .first()
    )

    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee with this email already exists",
        )

    db_employee = Employee(**employee.model_dump())

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return db_employee


def get_employee(db, employee_id):

    return db.query(Employee).filter(Employee.id == employee_id).first()


def get_employees(db, position=None, include_all=False, page=1, page_size=10):

    employees_q = db.query(Employee)

    if not include_all:
        employees_q = employees_q.filter(Employee.deactivated.is_(False))

    if position:
        employees_q = employees_q.filter(Employee.position == position)

    return employees_q.offset((page - 1) * page_size).limit(page_size).all()


def update_employee(db, employee_id, employee_data: EmployeeUpdate):

    employee = get_employee(db, employee_id)

    if not employee:
        return None

    update_data = employee_data.model_dump(
        exclude_unset=True,
    )

    if "email" in update_data:

        existing_employee = (
            db.query(Employee)
            .filter(Employee.email == update_data["email"])
            .filter(Employee.id != employee_id)
            .first()
        )

        if existing_employee:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee with this email already exists",
            )

    for key, value in update_data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee


def delete_employee(db, employee_id):

    employee = get_employee(db, employee_id)

    if not employee:
        return False

    employee.deactivated = True
    db.commit()

    return True


def average_salary(db):
    return round(db.query(func.avg(Employee.salary)).scalar(), 2)
