from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.student import Student
from app.cli.cli_helpers import print_model_table, print_join_table
from app.services.student_service import list_students
from app.models.student import Student
from app.models.parent import Parent 

def print_student_table(session: Session) -> None:
    students = list_students(session)
    
    print_model_table(
        items=students,
        columns=["id", "name", "status"],
        headers=["ID", "Name", "Status"],
        formatters={
            "name": format_name,
            "status": format_status 
        }
    )

def format_name(s: Student) -> str:
    return f"{s.forename} {s.surname}"

def format_status(s: Student) -> str:
    return "Active" if s.is_active else "Inactive"

def print_parents_with_students(session: Session) -> None:
    items = session.execute(select(Parent, Student).join(Parent.students)).all()

    print_join_table(
        rows=items,
        columns=[
            lambda t: t[0].id,
            lambda t: f"{t[0].forename} {t[0].surname}",
            lambda t: t[1].id,
            lambda t: f"{t[1].forename} {t[1].surname}",
        ],
        headers=["Parent ID", "Parent", "Student ID", "Student"]
    )