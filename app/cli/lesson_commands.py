from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from app.services.lesson_service import create_lesson, get_lesson, list_lessons, update_lesson, delete_lesson

def handle_lesson_menu():
    commands = WordCompleter(["add", "list", "update", "delete", "back"], ignore_case=True)

    while True:
        choice = prompt("Lessons > ", completer=commands).strip().lower()
        
        if choice == "add":
            print("Adding lesson... (not yet implemented)")
        elif choice == "list":
            print("Listing lessons... (not yet implemented)")
        if choice == "update":
            print("Updating lesson... (not yet implemented)")
        elif choice == "delete":
            print("Deleting lessons... (not yet implemented)")
        elif choice == "back":
            break
        else:
            print("Unknown command.")


def cli_create_lesson() -> None:
    try:
        rate_id = int(prompt("RateID: "))
        duration = float(prompt("Lesson duration (hours): "))
        date = prompt("Lesson date (leave blank for today's date): ")

        data = {}

        data["rate_id"] = rate_id
        data["duration"] = duration

    except

def cli_list_lessons() -> None:
    pass

def cli_update_lesson() -> None:
    pass

def cli_delete_lesson() -> None:
    pass
