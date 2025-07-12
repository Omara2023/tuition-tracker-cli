from sqlalchemy.orm import Session
from app.models.lesson import Lesson
from app.services.crud import create, list_all, get, update_data, delete

def create_lesson(session: Session, data: dict) -> Lesson:
    return create(session, Lesson, data)

def list_lessons(session: Session) -> list[Lesson]:
    return list_all(session, Lesson)

def get_lesson(session: Session, id: int) -> Lesson:
    return get(session, Lesson, id)

def update_lesson(session: Session, id: int, update: dict) -> Lesson | None:
    return update_data(session, Lesson, id, update)

def delete_lesson(session: Session, id: int) -> bool:
    return delete(session, Lesson, id)