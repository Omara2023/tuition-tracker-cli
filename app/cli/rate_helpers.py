from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.student import Student
from app.models.rate import Rate
from app.cli.cli_helpers import print_join_table

def print_rate_with_student(session: Session) -> None:
    items = session.execute(select(Student, Rate).join(Student.rates)).all()
    print_join_table(
        rows=items,
        columns=[
            lambda t: t[1].id,
            lambda t: f"{t[0].forename} {t[0].surname}",
            lambda t: t[1].level,
            lambda t: t[1].hourly_rate
        ],
        headers=["Rate ID", "Student", "Level", "Rate (£/Hour)"]
    )