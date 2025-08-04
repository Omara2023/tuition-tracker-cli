import os
import csv
from sqlalchemy import select
import app.db.models_registry
from app.db.cm import get_session
from app.models.parent import Parent
from app.models.student import Student
from app.models.rate import Rate, string_to_level_enum
from app.models.lesson import Lesson
from app.models.payment import Payment
from app.models.lesson_payment import LessonPayment

class DataInjector:
    """Wrapper class to read CSV's for inerstion to sqlite file."""

    def __init__(self, path_to_db: str, path_to_directory: str):
        self.path = path_to_db
        self.data_dir = path_to_directory

    def _insert_parents(self, filename: str) -> bool:
        try:    
            path = os.path.join(self.data_dir, filename)
            if not os.path.exists(path):
                raise ValueError("Invalid path.")
            
            with open(path, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                parents = [Parent(forename=row["Forename"], surname=row["Surname"]) for row in reader]
        
            with get_session() as session:
                session.add_all(parents)
            return True
        except Exception as e:
            print(f"Failed to insert parents {e}.")
            return False
                
    def _insert_students(self, filename: str) -> bool:
        """Add students from parent_student combined CSV."""
        try:    
            path = os.path.join(self.data_dir, filename)
            if not os.path.exists(path):
                raise ValueError("Invalid path.")
            
            students = list()
            with open(path, newline="") as csvfile:
                with get_session() as session:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        p_forename, p_surname = row["Forename_parent"], row["Surname_parent"]
                        parent_id = session.execute(select(Parent.id).where(Parent.forename == p_forename and Parent.surname == p_surname)).scalars().first()
                        if parent_id is None:
                            print(f"Failed to insert row: {row}")
                            continue

                        s_forename, s_surname, s_active = row["Forename_student"], row["Surname_student"], row["Active"] == "True"
                        students.append(Student(forename=s_forename, surname=s_surname, is_active=s_active, parent_id=parent_id))
                        
                    session.add_all(students)
            return True
        except Exception as e:
            print(f"Failed to insert students {e}.")
            return False

    def _insert_rates(self, filename: str) -> bool:
        """Add rates from rates CSV."""
        try:    
            path = os.path.join(self.data_dir, filename)
            if not os.path.exists(path):
                raise ValueError("Invalid path.")
            
            rates = list()
            with open(path, newline="") as csvfile:
                with get_session() as session:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        forename, surname = row["Forename"], row["Surname"]
                        student_id = session.execute(select(Student.id).where(Student.forename == forename and Student.surname == surname)).scalars().first()
                        if student_id is None:
                            print(f"Failed to insert row: {row}")
                            continue

                        level, rate = string_to_level_enum(row["Level"]), float(row["Hourly rate"])
                        rates.append(Rate(student_id=student_id, hourly_rate=rate, level=level))
                        
                    session.add_all(rates)
            return True
        except Exception as e:
            print(f"Failed to insert rates {e}.")
            return False

    def _insert_lessons(self) -> bool:
        pass

    def _insert_payments(self) -> bool:
        pass

if __name__ == "__main__":
    injector = DataInjector("app\\db\\app.db", "data")
    injector._insert_parents("parents.csv")
    injector._insert_students("parent_student.csv")
    injector._insert_rates("rates.csv")

