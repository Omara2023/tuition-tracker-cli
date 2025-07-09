from contextlib import contextmanager
from app.db.session import SessionLocal

@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()