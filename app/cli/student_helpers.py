from sqlalchemy.orm import Session
from app.models.student import Student
from app.cli.cli_helpers import print_model_table
from app.services.student_service import list_students

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
