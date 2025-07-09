from sqlalchemy.orm import Session
from models.student import Student
from services.crud import create, list_all, get, update_data, delete

def create_student(session: Session, data: dict) -> Student:
    return create(session, Student, data)

def list_students(session: Session) -> list[Student]:
    return list_all(session, Student)

def get_student(session: Session, id: int) -> Student:
    return get(session, Student, id)

def update_student(session: Session, id: int, update: dict) -> Student | None:
    return update_data(session, Student, id, update)

def delete_student(session: Session, id: int) -> bool:
    return delete(session, Student, id)