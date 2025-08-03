from sqlalchemy.orm import Session
from sqlalchemy import select

from app.cli.cli_helpers import print_model_table
from app.models.lesson import Lesson


def print_lessons(session: Session) -> None:
    lessons_exist = session.scalars((select(Lesson))).first() is not None
    if not lessons_exist:
        print("No lessons to print.")
    lessons = session.scalars(select(Lesson)).all()