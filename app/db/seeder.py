from sqlalchemy import select
from app.db.cm import get_session
from app.models.parent import Parent
from app.models.student import Student
from app.models.rate import Rate, RateLevel
from app.models.lesson import Lesson

class Seeder:
    """Basic seeder to populate database."""
    def seed_all(self) -> bool:
        return self._seed_parents() and self._seed_students() and self._seed_rates()

    def _seed_parents(self) -> bool:
        try:
            with get_session() as session:
                parents_exist = session.execute(select(Parent)).scalars().first() is not None
                if parents_exist:
                    print("Parents already seeded.")
                    return True   
                session.add_all([
                    Parent(forename="John", surname="Doe", is_active=True),
                    Parent(forename="Bob", surname="Jones", is_active=True),
                    Parent(forename="Jake", surname="Lockwood", is_active=False),
                    Parent(forename="Ben", surname="Kareem", is_active=False)
                ])
                print("Seeded parents.")
            return True
        except Exception as e:
            print(f"Error seeding parents: {e}")
            return False
        
    def _seed_students(self) -> bool:
        try:
            with get_session() as session:
                students_exist = session.execute(select(Student)).scalars().first() is not None 
                if students_exist:
                    print("Students already seeded.")
                    return True
                john = session.execute(select(Parent).where(Parent.forename == "John")).scalars().first()
                bob = session.execute(select(Parent).where(Parent.forename == "Bob")).scalars().first() 
                jake = session.execute(select(Parent).where(Parent.forename == "Jake")).scalars().first()
                ben  = session.execute(select(Parent).where(Parent.forename == "Ben")).scalars().first()
                
                if not john or not bob or not jake or not  ben: 
                    missing = [name for name, p in zip(["John", "Bob", "Jake", "Ben"], [john, bob, jake, ben]) if p is None]
                    print(f"Missing parents: {missing}")
                    return False
                
                session.add_all([
                    Student(forename="Jane", surname="Doe", is_active=True, parent_id=john.id),
                    Student(forename="Charlie", surname="Doe", is_active=True, parent_id=john.id),
                    Student(forename="Bobbington", surname="Jones", is_active=True, parent_id=bob.id),
                    Student(forename="Jimmy", surname="Lockwood", is_active=False, parent_id=jake.id),
                    Student(forename="Billy", surname="Kareem", is_active=False, parent_id=ben.id)
                ])

                print("Seeded students.")
            return True
                    
        except Exception as e:
            print(f"Error seeding students: {e}")
            return False
        
    def _seed_rates(self) -> bool:
        try:
            with get_session() as session:
                rates_exist = session.execute(select(Rate)).scalars().first() is not None
                if rates_exist:
                    print("Rates already seeded.")
                    return True

                students = session.execute(select(Student)).scalars().all()
                if not students:
                    print("No students found, cannot seed rates.")
                    return False

                rates = [
                    Rate(student_id=students[0].id, level=RateLevel.GCSE, hourly_rate=25.0),
                    Rate(student_id=students[0].id, level=RateLevel.A_LEVEL, hourly_rate=30.0),
                    Rate(student_id=students[1].id if len(students) > 1 else students[0].id, level=RateLevel.GCSE, hourly_rate=20.0),
                    Rate(student_id=students[2].id if len(students) > 2 else students[0].id, level=RateLevel.A_LEVEL, hourly_rate=28.0),
                    Rate(student_id=students[3].id if len(students) > 3 else students[0].id, level=RateLevel.A_LEVEL, hourly_rate=35.0),
                ]

                session.add_all(rates)
                print("Seeded rates.")
            return True
        except Exception as e:
            print(f"Error seeding rates: {e}")
            return False


if __name__ == "__main__":
    seeder = Seeder()
    if seeder.seed_all():
        print("Seeding successfull.")
    else:
        print("Seeding failed.")
            