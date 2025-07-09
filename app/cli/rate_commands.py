from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

def handle_rate_menu():
    commands = WordCompleter(["add", "list", "update", "delete", "back"], ignore_case=True)

    while True:
        choice = prompt("Rates > ", completer=commands).strip().lower()
        
        if choice == "add":
            print("Adding rate... (not yet implemented)")
        elif choice == "list":
            print("Listing rates... (not yet implemented)")
        if choice == "update":
            print("Updating rate... (not yet implemented)")
        elif choice == "delete":
            print("Deleting rate... (not yet implemented)")
        elif choice == "back":
            break
        else:
            print("Unknown command.")
