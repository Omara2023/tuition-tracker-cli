from sqlalchemy import select
from datetime import datetime, date, timedelta
from random import randint
from app.db.cm import get_session
from app.models.parent import Parent
from app.models.student import Student
from app.models.rate import Rate, RateLevel
from app.models.lesson import Lesson, Subjects
from app.models.payment import Payment
from app.models.lesson_payment import LessonPayment

class Seeder:
    """Basic seeder to populate database."""
    def seed_all(self) -> bool:
        return self._seed_parents() and self._seed_students() and self._seed_rates() and self._seed_lessons() and self._seed_payments()

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
                    Rate(student_id=students[1].id, level=RateLevel.GCSE, hourly_rate=20.0),
                    Rate(student_id=students[2].id, level=RateLevel.A_LEVEL, hourly_rate=28.0),
                    Rate(student_id=students[3].id, level=RateLevel.A_LEVEL, hourly_rate=35.0),
                ]

                session.add_all(rates)
                print("Seeded rates.")
            return True
        except Exception as e:
            print(f"Error seeding rates: {e}")
            return False
        
    def _seed_lessons(self) -> bool:
        try:
            with get_session() as session:
                lessons_exist = session.execute(select(Lesson)).scalars().first() is not None
                if lessons_exist:
                    print("Lessons already seeded.")
                    return True

                rates = session.execute(select(Rate)).scalars().all()
                if not rates:
                    print("No rates found, cannot seed lessons.")
                    return False
                
                lesson_dates = [
                    date(2025, 7, 10),
                    date(2025, 7, 15),
                    date(2025, 7, 20),
                    date(2025, 7, 25),
                    date(2025, 7, 30),
                ]
                
                lessons = [
                    Lesson(
                        rate_id=rates[0].id,
                        subject=Subjects.MATHEMATICS,
                        duration=1.5,
                        date=lesson_dates[0]
                    ),
                    Lesson(
                        rate_id=rates[0].id,
                        subject=Subjects.PHYSICS,
                        duration=2.0,
                        date=lesson_dates[1]
                    ),
                    Lesson(
                        rate_id=rates[1].id,
                        subject=Subjects.CHEMISTRY,
                        duration=1.0,
                        date=lesson_dates[2]
                    ),
                    Lesson(
                        rate_id=rates[1].id,
                        subject=Subjects.BIOLOGY,
                        duration=1.5,
                        date=lesson_dates[3]
                    ),
                    Lesson(
                        rate_id=rates[2].id,
                        subject=Subjects.MATHEMATICS,
                        duration=2.0,
                        date=lesson_dates[4]
                    ),
                ]

                session.add_all(lessons)
                print("Seeded lessons.")
            return True
        except Exception as e:
            print(f"Error seeding lessons: {e}")
            return False
        
    def _seed_payments(self) -> bool:
        try:
            with get_session() as session:
                payments_exist: bool = session.execute(select(Payment)).scalars().first() is not None
                if payments_exist:
                    print("Payments already seeded.")
                    return True
                lessons = session.execute(select(Lesson)).scalars().all() 
                if not lessons:
                    print("No lessons to seed payments for.")
                    return False

                payments: list[Payment] = list()

                for lesson in lessons:
                    parent = lesson.rate.student.parent
                    delay = timedelta(days=randint(1, 10))
                    payment_time = datetime(year=lesson.date.year, month=lesson.date.month, day=lesson.date.day, hour=randint(0, 23), minute=randint(0, 59)) + delay
                    cost = lesson.rate.hourly_rate * lesson.duration

                    payment = Payment(parent_id=parent.id, timestamp=payment_time, amount=cost)
                    payments.append(payment)

                session.add_all(payments)
            print("Successfully seeded payments.")
            return True
        except Exception as e:
            print(f"Error seeding payments {e}.")
            return False

    def _link_lessons_to_payments(self) -> bool:
        """Returns if all lessons were successfully linked to and covered fully by a payment."""
        failed = False
        with get_session() as session:
            lessons = session.execute(select(Lesson)).scalars().all()
            for lesson in lessons:
                payment, available_amount = self._get_compatible_payment(lesson)
                if payment is None:
                    print(f"No valid payment exists to cover this lesson: {lesson}.")
                    failed = True
                    continue
                
                lesson_cost = lesson.rate.hourly_rate * lesson.duration
                if lesson_cost == 0: continue
                    
                if lesson_cost <= available_amount: #case 1: lesson can be paid in full by the remainder of this payment.
                    session.add(LessonPayment(lesson_id=lesson.id, payment_id=payment.id, amount_paid=lesson_cost)) 
                else: #case 2: lesson cannot be covered by current payment alone.
                    session.add(LessonPayment(lesson_id=lesson.id, patment_id=payment.id, amount_paid=available_amount))
                    lesson_cost -= available_amount
                    while (lesson_cost > 0) :
                        payment, available_amount = self._get_compatible_payment(lesson)
                        if payment is None:
                            failed = True
                            print(f"No more valid payments exist to cover this lesson: {lesson}.")
                            break
                        amount_to_contribute = min(lesson_cost, payment.amount)
                        session.add(LessonPayment(lesson_id=lesson, payment_id=payment.id, amount_paid=amount_to_contribute))
                        lesson_cost -= amount_to_contribute
                    
            if failed:
                print("Linking lessons to payments fully has failed.")
            else:
                print("All lessons successfully linked to payments and covered in full.")

            return failed

    def _get_compatible_payment(self, lesson: Lesson) -> tuple[Payment | None, float]:
        with get_session() as session:
            parent = lesson.rate.student.parent
            candidate_payments = session.execute(select(Payment).where(Payment.parent_id == parent.id)).scalars().all()
            for payment in candidate_payments:
                lesson_payments = session.execute(select(LessonPayment).where(LessonPayment.payment_id == payment.id)).scalars().all()
                total_payment_value_used = sum([lp.amount_paid for lp in lesson_payments])
                if total_payment_value_used < payment.amount:
                    return payment, payment.amount - total_payment_value_used
            return None, 0
                
if __name__ == "__main__":
    seeder = Seeder()
    if seeder.seed_all():
        print("Seeding successfull.")
    else:
        print("Seeding failed.")
            