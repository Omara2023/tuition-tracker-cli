from sqlalchemy.orm import Session
from sqlalchemy import select
from app.cli.cli_helpers import print_join_table
from app.models.student import Student
from app.models.rate import Rate
from app.models.lesson import Lesson

def print_lessons_with_student_and_rate(session: Session) -> None:
    items = session.execute(select(Student, Rate, Lesson).join(Student.rates).join(Rate.lessons).order_by(Student.forename, Student.surname)).all() 
    if not items:
        print("No lessons to display.")
        return
    
    print_join_table(
        rows=items,
        columns=[
            lambda t: t[2].id,
            lambda t: f"{t[0].forename} {t[0].surname}",
            lambda t: str(t[2].date),
            lambda t: t[1].level,
            lambda t: t[2].subject,
            lambda t: t[1].hourly_rate,
            lambda t: t[2].duration,
            lambda t: round(t[2].cost(), 2),
        ],
        headers=["ID", "Student", "Date", "Level", "Subject", "Rate", "Length", "Cost"] #paid for status via querying payment?????
    )