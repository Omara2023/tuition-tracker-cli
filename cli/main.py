from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

main_commands = WordCompleter(["parents", "students", "lessons", "payments", "exit", "quit"], ignore_case=True)

def main_loop() -> None:
    """Main CLI loop."""
    while True:
        choice = prompt("Main > ", completer=main_commands).strip().lower()

        if choice == "parents":
            break