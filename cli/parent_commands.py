from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

def handle_parent_menu():
    commands = WordCompleter(["add", "list", "update", "delete", "back"], ignore_case=True)

    while True:
        choice = prompt("Parents > ", completer=commands).strip().lower()
        
        if choice == "add":
            print("Adding parent... (not yet implemented)")
        elif choice == "list":
            print("Listing parents... (not yet implemented)")
        if choice == "update":
            print("Updating parent... (not yet implemented)")
        elif choice == "delete":
            print("Deleting parent... (not yet implemented)")
        elif choice == "back":
            break
        else:
            print("Unknown command.")
