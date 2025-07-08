from sqlalchemy.orm import Session
from models.parent import Parent

def create_parent(session: Session, data: dict) -> Parent:
    parent = Parent(**data)
    session.add(parent)
    session.flush()
    session.refresh(parent)
    return parent

def list_parents(session: Session) -> list[Parent]:
    return session.query(Parent).all()

def get_parent(session: Session, id: int) -> Parent:
    return session.get(Parent, id)

def update_parent(session: Session, id: int, update: dict) -> Parent | None:
    parent = session.get(Parent, id)
    if not parent:
        return None

    for key, value in update.items():
        if hasattr(parent, key):
            setattr(parent, key, value)

    session.flush()
    session.refresh(parent)
    return parent

def delete_parent(session: Session, id: int) -> bool:
    parent = session.get(Parent, id)
    if not parent:
        return False
    session.delete(parent)
    return True