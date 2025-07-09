from sqlalchemy.orm import Session

def create(session: Session, model_class, data: dict):
    obj = model_class(**data)
    session.add(obj)
    session.flush()
    session.refresh(obj)
    return obj

def list_all(session: Session, model_class):
    return session.query(model_class).all()

def get(session: Session, model_class, id: int):
    return session.get(model_class, id)

def update_data(session: Session, model_class, id: int, updates: dict):
    obj = session.get(model_class, id)
    if not obj:
        return None
    for key, value in updates.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
    session.flush()
    session.refresh(obj)
    return obj

def delete(session: Session, model_class, id: int):
    obj = session.get(model_class, id)
    if not obj:
        return False
    session.delete(obj)
    return True