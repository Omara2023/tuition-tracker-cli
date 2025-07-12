from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from app.db.cm import get_session
from app.services.rate_service import create_rate, list_rates, get_rate, update_rate, delete_rate
from app.services.student_service import get_student
from app.models.rate import string_to_level_enum

def handle_rate_menu():
    commands = WordCompleter(["add", "list", "update", "delete", "back"], ignore_case=True)

    while True:
        choice = prompt("Rates > ", completer=commands).strip().lower()
        
        if choice == "add":
            cli_create_rate()
        elif choice == "list":
            cli_list_rates()
        if choice == "update":
            cli_update_rate()
        elif choice == "delete":
            cli_delete_rate()
        elif choice == "back":
            break
        else:
            print("Unknown command.")

def cli_create_rate() -> None:
    try:
        student_id = int(prompt("Student ID: ").strip())
        level = prompt("Level ").strip()
        rate = float(prompt("Hourly rate (GBP): ").strip().lower())
    
        data = {}

        if not student_id or not level or not rate:
            raise ValueError

        data["student_id"] = student_id
        data["level"] = string_to_level_enum(level)        
        data["hourly_rate"] = rate

        with get_session() as db:
            if not get_student(db, student_id):
                print("Invalid student ID.")
                return
            created = create_rate(db, data)
            if created:
                print(f"Created rate: {created.id}")
            else:
                print("Failed to create rate.")

    except ValueError:
        print("Invalid input.")
    except Exception as e:
        print(f"Failed to create rate: {e}")

def cli_list_rates() -> None:
    try:
        with get_session() as db:
            rates = list_rates(db)
            if rates:
                for i in rates:
                    print(i)
            else:
                print("Zero rates to list.")
    except Exception as e:
        print(f"Failed to retrieve rates {e}.")

def cli_update_rate() -> None:
    try:
        id = int(prompt("Enter rate ID to update: "))
        student_id = int(prompt("New student_id (leave blank to skip): ").strip())
        level = prompt("New level: GCSE or A-LEVEL (leave blank to skip): ").strip()
        hourly_rate = prompt("New hourly rate: (leave blank to skip): ").strip().lower()

        updates = dict()

        if student_id:
            updates["student_id"] = student_id
        if level:
            updates["level"] = string_to_level_enum(level)
        if hourly_rate:
            updates["rate"] = float(hourly_rate)

        with get_session() as db:
            updated = update_rate(db, id, updates)
            if updated:
                print(f"Updated rate: {updated.id}")
            else:
                print("Rate not found.")

    except ValueError:
        print("Invalid input.")

def cli_delete_rate() -> None:
    try:
        id = int(prompt("Enter rate ID to delete: "))

        with get_session() as db: 
            to_delete = get_rate(db, id)
            choice = prompt(f"Are you sure you want to delete rate {to_delete.id} (yes or no)?").strip().lower()
            if choice in ["y", "yes"]:
                if delete_rate(db, id):
                    print("Successfully deleted rate.")
                else:
                    print("Failed to delete rate.")
            
    except ValueError:
        print("Invalid rate id.")

