from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from collections import defaultdict
from random import randint, choices, sample, choice
from faker import Faker
from app.db.cm import get_session
from app.models.parent import Parent
from app.models.student import Student
from app.models.rate import Rate, RateLevel
from app.models.lesson import Lesson, Subjects
from app.models.payment import Payment
from app.models.lesson_payment import LessonPayment

class Seeder:
    """Basic seeder to populate database."""

    def __init__(self) -> None:
        self.faker = Faker()

    def seed_all(self) -> bool:
        return self._seed_parents() and self._seed_students() and self._seed_rates() and self._seed_lessons() and self._seed_payments()

    def _make_parent(self) -> Parent:
        return Parent(
            forename=self.faker.first_name(),
            surname=self.faker.last_name(),
            is_active=self.faker.boolean(chance_of_getting_true=75)
        )
    
    def _make_student(self, parent_id: int) -> Student:
        return Student(
            forename=self.faker.first_name(),
            surname=self.faker.last_name(),
            is_active=self.faker.boolean(chance_of_getting_true=80),
            parent_id=parent_id
        )

    def _seed_parents(self, num_parents: int = 10) -> bool:
        try:
            with get_session() as session:
                parents_exist = session.execute(select(Parent)).scalars().first() is not None
                if parents_exist:
                    print("Parents already seeded.")
                    return True  

                parents = [self._make_parent() for _ in range(num_parents)] 
                session.add_all(parents)
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
                
                students = []
                parents = session.execute(select(Parent).where(Parent)).scalars().all()
                
                for parent in parents:
                    for _ in range(randint(1, 3)):
                        students.append(self._make_student(parent.id))
                
                session.add_all(students)
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
                    print("No students found.")
                    return False

                rates = []
                levels = [RateLevel.GCSE, RateLevel.A_LEVEL]

                for student in students:
                    num_rates = randint(1,2)
                    assigned_levels = sample(levels, k=num_rates)
                    for level in assigned_levels:
                        hourly_rate = round(randint(400, 1000) * 0.05, 2) #£20.00–£50.00
                        rates.append(Rate(
                            student_id=student.id, 
                            level=level, 
                            hourly_rate=hourly_rate
                        ))
                       
                session.add_all(rates)
                print("Seeded rates.")
            return True
        except Exception as e:
            print(f"Error seeding rates: {e}")
            return False
        
    def _seed_lessons(self, num_lessons: int = 25) -> bool:
        try:
            with get_session() as session:
                lessons_exist = session.execute(select(Lesson)).scalars().first() is not None
                if lessons_exist:
                    print("Lessons already seeded.")
                    return True

                rates = session.execute(select(Rate)).scalars().all()
                if not rates:
                    print("No rates found.")
                    return False
                
                lesson_subjects = list(Subjects)
                
                lessons = []

                for _ in range(num_lessons):
                    rate = choice(rates)
                    subject = choice(lesson_subjects)
                    duration = choice([1.0, 1.5, 2.0])

                    days_ago = randint(0, 60)
                    lesson_date = date.today() - timedelta(days=days_ago)

                    lessons.append(Lesson(
                        rate_id=rate.id,
                        subject=subject,
                        duration=duration,
                        date=lesson_date
                    ))

            session.add_all(lessons)
            print(f"Seeded {len(lessons)} random lessons.")
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

                parent_to_lessons: dict[int, list[Lesson]] = defaultdict(list)

                for lesson in lessons:
                    parent_id = lesson.rate.student.parent.id
                    parent_to_lessons[parent_id].append(lesson)

                def random_time(base_date: date) -> datetime:
                    delay = timedelta(days=randint(1, 15), hours=randint(0,23), minutes=randint(0, 59))
                    return datetime.combine(base_date, datetime.min.time()) + delay
                    
                strategies = ["full", "partial", "per_lesson", "none"]
                weights = [0.3, 0.3, 0.3, 0.1]

                payments = []

                for parent_id, parent_lessons in parent_to_lessons.items():
                    if not parent_lessons:
                        continue
                        
                    strategy = choices(strategies, weights, k=1)[0]
                    base_date = min(l.date for l in parent_lessons)

                    match strategy:
                        case "none":
                            print(f"Parent {parent_id} will not pay.")
                            continue
                        case "full":
                            total = sum(l.rate.hourly_rate * l.duration for l in parent_lessons)
                            payments.append(Payment(
                                parent_id=parent_id, 
                                amount=round(total, 2),
                                timestamp=random_time(base_date)
                            ))
                            print(f"Parent {parent_id}: full payment for all lessons.")
                        case "partial":
                            subset = sample(parent_lessons, k=randint(1, len(parent_lessons)))
                            total = sum(l.rate.hourly_rate * l.duration for l in subset)
                            payments.append(Payment(
                                parent_id=parent_id, 
                                amount=round(total, 2),
                                timestamp=random_time(base_date)
                            ))
                            print(f"Parent {parent_id}: partial payment for {len(subset)} lesson(s).")
                        case "per_lesson":
                            for lesson in parent_lessons:
                                base_amount = lesson.rate.hourly_rate * lesson.duration
                                fuzzed_amount = round(base_amount * randint(80, 110) / 100, 2)
                                payments.append(Payment(
                                parent_id=parent_id,
                                amount=fuzzed_amount,
                                timestamp=random_time(lesson.date)
                            ))
                            print(f"Parent {parent_id}: paid per lesson ({len(parent_lessons)} payments).")

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
                lesson_cost = lesson.rate.hourly_rate * lesson.duration
                if lesson_cost == 0:
                    print(f"Zero cost lesson skipped: {lesson.id}")
                    continue

                while lesson_cost > 0:
                    payment, available = self._get_compatible_payment(lesson, session)
                    if payment is None:
                        print(f"Cannot fully cover lesson {lesson.id}")
                        failed = True
                        break

                    to_pay = min(lesson_cost, available)
                    session.add(LessonPayment(lesson_id=lesson.id, payment_id=payment.id, amount_paid=to_pay))
                    session.flush()
                    lesson_cost -= to_pay

        print("Linking complete." if not failed else "Linking incomplete.")
        return not failed

    def _get_compatible_payment(self, lesson: Lesson, session: Session) -> tuple[Payment | None, float]:
        parent_id = lesson.rate.student.parent.id
        payments = session.execute(select(Payment).where(Payment.parent_id == parent_id)).scalars().all()
        for payment in payments:
            used = session.execute(select(LessonPayment.amount_paid).where(LessonPayment.payment_id == payment.id)).scalars().all()
            remaining = payment.amount - sum(used)
            if remaining > 0:
                return payment, remaining
        return None, 0
                
if __name__ == "__main__":
    seeder = Seeder()
    if seeder.seed_all():
        print("Seeding successfull.")
    else:
        print("Seeding failed.")
            