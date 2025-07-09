from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from cli.parent_commands import handle_parent_menu
from cli.student_commands import handle_student_menu
from cli.rate_commands import handle_rate_menu
from cli.lesson_commands import handle_lesson_menu
from cli.payment_commands import handle_payment_menu

main_commands = WordCompleter(["parents", "students", "rates", "lessons", "payments", "exit", "quit"], ignore_case=True)

def main_loop() -> None:
    """Main CLI loop."""
    while True:
        choice = prompt("Main > ", completer=main_commands).strip().lower()

        if choice == "parents":
            handle_parent_menu()
        elif choice == "students":
            handle_student_menu()
        elif choice == "rates":
            handle_rate_menu()
        elif choice == "lessons":
            handle_lesson_menu()
        elif choice == "payments":
            handle_payment_menu()
        elif choice == "exit" or choice == "quit":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try 'parents', 'students', 'rates', 'lessons', 'payments', 'exit' or 'quit'.")

if __name__ == "__main__":
    main_loop()