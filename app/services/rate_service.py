from sqlalchemy.orm import Session
from app.models.rate import Rate 
from app.services.crud import create, list_all, get, update_data, delete

def create_rate(session: Session, data: dict) -> Rate:
    return create(session, Rate, data)

def list_rates(session: Session) -> list[Rate]:
    return list_all(session, Rate)

def get_rate(session: Session, id: int) -> Rate:
    return get(session, Rate, id)

def update_rate(session: Session, id: int, update: dict) -> Rate | None:
    return update_data(session, Rate, id, update)

def delete_rate(session: Session, id: int) -> bool:
    return delete(session, Rate, id)