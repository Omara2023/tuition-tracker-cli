from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from datetime import datetime
from app.db.cm import get_session
from app.services.lesson_service import create_lesson, get_lesson, update_lesson, delete_lesson
from app.services.rate_service import get_rate
from app.models.lesson import string_to_subject_enum
from app.cli.cli_helpers import ask_required_int, ask_required_string, ask_required_float, ask_optional_int, ask_optional_string, ask_optional_float, ask_required_bool
from app.cli.rate_helpers import print_rate_with_student
from app.cli.lesson_helpers import print_lessons_with_student_and_rate

def handle_lesson_menu():
    commands = WordCompleter(["add", "list", "update", "delete", "back"], ignore_case=True)

    print("Lessons: 'add', 'list', 'update', 'delete' or 'back'.")
    while True:
        choice = prompt("Lessons > ", completer=commands).strip().lower()
        
        if choice == "add":
            cli_create_lesson()
        elif choice == "list":
            cli_list_lessons()
        elif choice == "update":
            cli_update_lesson()
        elif choice == "delete":
            cli_delete_lesson()
        elif choice == "back":
            break
        else:
            print("Unknown command.")

def cli_create_lesson() -> None:
    try:
        with get_session() as session:
            print_rate_with_student(session)

            rate_id = ask_required_int("Rate ID")
            subject = ask_required_string("Subject")
            duration = ask_required_float("Lesson duration (hours)")
            date = ask_required_string("Lesson date (yyyy-mm-dd) (leave blank for today's date)")

            data = {}

            data["rate_id"] = rate_id
            data["subject"] = string_to_subject_enum(subject)
            data["duration"] = duration
            data["date"] = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()

            rate = get_rate(session, rate_id)
            if not rate:
                print("Invalid Rate.")
                return
            created = create_lesson(session, data)
            if created:
                print(f"Sucessfully created lesson: {created}")
            else:
                raise Exception

    except Exception as e:
        print(f"Failed to create lesson: {e}")

def cli_list_lessons() -> None:
    try:
        with get_session() as session:
            print_lessons_with_student_and_rate(session)
    except Exception as e:
        print(f"Failed to list lessons: {e}")

def cli_update_lesson() -> None:
    try:
        with get_session() as session:
            print_lessons_with_student_and_rate(session)
            id = ask_required_int("Lesson ID of lesson to edit")

            print_rate_with_student(session)
            rate_id = ask_optional_int("New RateID (leave blank to skip)")
            subject = ask_optional_string("New subject (leave blank to skip)")
            duration = ask_optional_float("New lesson duration in hours (leave blank to skip)")
            date = ask_optional_string("New lesson date (yyyy-mm-dd) (leave blank to skip)")

            data = {}

            if rate_id: data["rate_id"] = rate_id
            if subject: data["subject"] = string_to_subject_enum(subject)
            if duration: data["duration"] = duration
            if date: data["date"] = datetime.strptime(date, "%Y-%m-%d")

            updated = update_lesson(session, id, data)
            if updated:
                print(f"Lessons successfully updated: {updated}.")
            else:
                print("Failed to update lesson.")

    except Exception as e:
        print(f"Failed to update lesson: {e}.")


def cli_delete_lesson() -> None:
    try:
        with get_session() as session: 
            print_lessons_with_student_and_rate(session)

            id = ask_required_int("Enter LessonID of lesson to delete: ") 
            to_delete = get_lesson(session, id)
            if not to_delete:
                print(f"No lesson exists with id {id}.")
                return
            choice = ask_required_bool(f"Are you sure you want to delete lesson {to_delete.id} (yes or no)?", default=False)
            if choice:
                if delete_lesson(session, id):
                    print("Successfully deleted lesson.")
                else:
                    print("Failed to delete lesson.")
            
    except ValueError:
        print("Invalid LessonID.")
