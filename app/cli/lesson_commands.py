from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from datetime import datetime
from app.db.cm import get_session
from app.services.lesson_service import create_lesson, get_lesson, list_lessons, update_lesson, delete_lesson
from app.services.rate_service import get_rate
from app.models.lesson import string_to_subject_enum

def handle_lesson_menu():
    commands = WordCompleter(["add", "list", "update", "delete", "back"], ignore_case=True)

    while True:
        choice = prompt("Lessons > ", completer=commands).strip().lower()
        
        if choice == "add":
            cli_create_lesson()
        elif choice == "list":
            cli_list_lessons()
        if choice == "update":
            cli_update_lesson()
        elif choice == "delete":
            cli_delete_lesson()
        elif choice == "back":
            break
        else:
            print("Unknown command.")

def cli_create_lesson() -> None:
    try:
        rate_id = int(prompt("RateID: "))
        subject = prompt("Subject: ")
        duration = float(prompt("Lesson duration (hours): "))
        date = prompt("Lesson date (yyyy-mm-dd) (leave blank for today's date): ")

        data = {}

        data["rate_id"] = rate_id
        data["subject"] = string_to_subject_enum(subject)
        data["duration"] = duration
        data["date"] = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()

        with get_session() as db:
            rate = get_rate(db, rate_id)
            if not rate:
                print("Invalid RateID.")
                return
            created = create_lesson(db, data)
            if created:
                print(f"Sucessfully created lesson: {created}")
            else:
                raise 

    except Exception as e:
        print(f"Failed to create lesson: {e}")

def cli_list_lessons() -> None:
    try:
        with get_session() as db:
            lessons = list_lessons(db)
            if not lessons:
                print("Zero lessons retrieved.")
                return
            for i in lessons:
                print(i)
    except Exception as e:
        print(f"Failed to retrieve lessons: {e}.")

def cli_update_lesson() -> None:
    try:
        id = int(prompt("LessonID of lesson to edit: "))
        rate_id = prompt("New RateID (leave blank to skip): ")
        subject = prompt("New subject (leave blank to skip): ")
        duration = prompt("New lesson duration in hours (leave blank to skip): ")
        date = prompt("New lesson date (yyyy-mm-dd) (leave blank to skip): ")

        data = {}

        if rate_id:
            data["rate_id"] = int(rate_id)
        if subject:
            data["subject"] = string_to_subject_enum(subject)
        if duration:
            data["duration"] = float(duration)
        if date:
            data["date"] = datetime.strptime(date, "%Y-%m-%d")

        with get_session() as db:
            updated = update_lesson(db, id, data)
            if updated:
                print(f"Lessons successfully updated: {updated}.")
            else:
                print("Failed to update lesson.")

    except Exception as e:
        print(f"Failed to update lesson: {e}.")


def cli_delete_lesson() -> None:
    try:
        id = int(prompt("Enter LessonID of lesson to delete: "))

        with get_session() as db: 
            to_delete = get_lesson(db, id)
            if not to_delete:
                print(f"No lesson exists with id {id}.")
                return
            choice = prompt(f"Are you sure you want to delete lesson {to_delete.id} (yes or no)? ").strip().lower()
            if choice in ["y", "yes"]:
                if delete_lesson(db, id):
                    print("Successfully deleted lesson.")
                else:
                    print("Failed to delete lesson.")
            
    except ValueError:
        print("Invalid LessonID.")
