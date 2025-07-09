from sqlalchemy.orm import Session
from app.models.parent import Parent
from app.services.crud import create, list_all, get, update_data, delete

def create_parent(session: Session, data: dict) -> Parent:
    return create(session, Parent, data)

def list_parents(session: Session) -> list[Parent]:
    return list_all(session, Parent)

def get_parent(session: Session, id: int) -> Parent:
    return get(session, Parent, id)

def update_parent(session: Session, id: int, update: dict) -> Parent | None:
    return update_data(session, Parent, id, update)

def delete_parent(session: Session, id: int) -> bool:
    return delete(session, Parent, id)