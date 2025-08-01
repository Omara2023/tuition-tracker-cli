from typing import Type
from sqlalchemy import delete, select
from sqlalchemy.orm import DeclarativeMeta
from app.db.cm import get_session
from app.models.lesson import Lesson
from app.models.rate import Rate
from app.models.student import Student
from app.models.parent import Parent

class Unseeder:
    """Basic unseeder to clear the database."""
    def _unseed(self, model_class: Type[DeclarativeMeta], class_name: str) -> bool:
        try:
            with get_session() as session:
                instances_exist = session.execute(select(model_class)).scalars().first() is not None
                if not instances_exist:
                    print(f"No {class_name}s to delete.")
                    return True
                session.execute(delete(model_class))
                print(f"Deleted all {class_name}s.")
                return True
        except Exception as e:
            print(f"Error deleting {class_name}: {e}")
            return False
    
    def _unseed_lessons(self) -> bool:
        return self._unseed(Lesson, "lesson")

    def _unseed_rates(self) -> bool:
        return self._unseed(Rate, "rate")
    
    def _unseed_students(self) -> bool:
        return self._unseed(Student, "student")

    def _unseed_parents(self) -> bool:
        return self._unseed(Parent, "parent")

    def unseed_all(self) -> bool:
        return (
            self._unseed_lessons() and
            self._unseed_rates() and
            self._unseed_students() and
            self._unseed_parents()
        )

if __name__ == "__main__":
    unseeder = Unseeder()
    unseeder.unseed_all()
