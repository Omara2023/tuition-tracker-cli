from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

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
