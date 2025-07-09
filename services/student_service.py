from sqlalchemy.orm import Session
from models.student import Student

def create_student(session: Session, data: dict) -> Student:
    student = Student(**data)
    session.add(student)
    session.flush()
    session.refresh(student)
    return student

def list_students(session: Session) -> list[Student]:
    return session.query(Student).all()

def get_student(session: Session, id: int) -> Student:
    return session.get(Student, id)

def update_student(session: Session, id: int, update: dict) -> Student | None:
    student = session.get(Student, id)
    if not student:
        return None

    for key, value in update.items():
        if hasattr(student, key):
            setattr(student, key, value)

    session.flush()
    session.refresh(student)
    return student

def delete_student(session: Session, id: int) -> bool:
    student = session.get(Student, id)
    if not student:
        return False
    session.delete(student)
    return True