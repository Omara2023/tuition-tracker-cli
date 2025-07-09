from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

def handle_payment_menu():
    commands = WordCompleter(["add", "list", "back"], ignore_case=True)

    while True:
        choice = prompt("Payments > ", completer=commands).strip().lower()
        
        if choice == "add":
            # collect input via prompt()
            print("Adding payment... (not yet implemented)")
        elif choice == "list":
            print("Listing payments... (not yet implemented)")
        elif choice == "back":
            break
        else:
            print("Unknown command.")
