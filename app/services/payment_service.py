from sqlalchemy.orm import Session
from app.models.payment import Payment
from app.services.crud import create, list_all, get, update_data, delete

def create_payment(session: Session, data: dict) -> Payment:
    return create(session, Payment, data)

def list_payment(session: Session) -> list[Payment]:
    return list_all(session, Payment)

def get_payment(session: Session, id: int) -> Payment:
    return get(session, Payment, id)

def update_payment(session: Session, id: int, update: dict) -> Payment | None:
    return update_data(session, Payment, id, update)

def delete_payment(session: Session, id: int) -> bool:
    return delete(session, Payment, id)