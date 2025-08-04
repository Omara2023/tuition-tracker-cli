from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from decimal import Decimal
from app.db.cm import get_session
from app.services.rate_service import create_rate, get_rate, update_rate, delete_rate
from app.cli.cli_helpers import ask_required_int, ask_required_string, ask_required_float, ask_optional_float, ask_optional_string, ask_required_bool
from app.cli.rate_helpers import print_rate_with_student
from app.cli.student_helpers import print_parents_with_students
from app.services.student_service import get_student
from app.models.rate import string_to_level_enum

def handle_rate_menu():
    commands = WordCompleter(["add", "list", "update", "delete", "back"], ignore_case=True)

    print("Rates: 'add', 'list', 'update', 'delete' or 'back'.")
    while True:
        choice = prompt("Rates > ", completer=commands).strip().lower()
        
        if choice == "add":
            cli_create_rate()
        elif choice == "list":
            cli_list_rates()
        elif choice == "update":
            cli_update_rate()
        elif choice == "delete":
            cli_delete_rate()
        elif choice == "back":
            break
        else:
            print("Unknown command.")

def cli_create_rate() -> None:
    try:
        with get_session() as session:
            print_parents_with_students(session)
            
            student_id = ask_required_int("Student ID")
            level = ask_required_string("Level")
            rate = ask_required_float("Hourly rate (GBP)")
        
            data = {}

            data["student_id"] = student_id
            data["level"] = string_to_level_enum(level)        
            data["hourly_rate"] = Decimal(str(rate))

            if not get_student(session, student_id):
                print("Invalid Student ID.")
                return
            created = create_rate(session, data)
            if created:
                print(f"Created rate: {created}")
            else:
                print("Failed to create rate.")

    except ValueError:
        print("Invalid input.")
    except Exception as e:
        print(f"Failed to create rate: {e}")

def cli_list_rates() -> None:
    try:
        with get_session() as session:
            print_rate_with_student(session)
    except Exception as e:
        print(f"Failed to retrieve rates {e}.")

def cli_update_rate() -> None:
    try:

        id = ask_required_int("Enter RateID to update")
        student_id = ask_optional_string("New StudentID (leave blank to skip)")
        level = ask_optional_string("New level: GCSE or A-LEVEL (leave blank to skip)")
        hourly_rate = ask_optional_float("New hourly rate: (leave blank to skip)")

        updates = dict()

        if student_id: updates["student_id"] = int(student_id)
        if level: updates["level"] = string_to_level_enum(level)
        if hourly_rate: updates["hourly_rate"] = Decimal(str(hourly_rate))

        with get_session() as db:
            updated = update_rate(db, id, updates)
            if updated:
                print(f"Updated rate: {updated}")
            else:
                print("Rate not found.")

    except ValueError:
        print("Invalid input.")

def cli_delete_rate() -> None:
    try:
        with get_session() as session: 
            print_rate_with_student(session)
            id = ask_required_int("Enter rate ID to delete: ")
            to_delete = get_rate(session, id)
            choice = ask_required_bool(f"Are you sure you want to delete rate {to_delete.id} (yes or no)?")
            if choice:
                if delete_rate(session, id):
                    print("Successfully deleted rate.")
                else:
                    print("Failed to delete rate.")
            
    except ValueError:
        print("Invalid rate id.")

