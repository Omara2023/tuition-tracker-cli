from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from app.db.cm import get_session
from app.services.student_service import create_student, list_students, get_student, update_student, delete_student
from app.services.parent_service import get_parent
from app.cli.cli_helpers import ask_required_bool, ask_optional_bool, ask_required_string, ask_optional_string, ask_required_int
from app.cli.student_helpers import print_student_table, print_parents_with_students
from app.cli.parent_helpers import select_parent

def handle_student_menu() -> None:
    commands = WordCompleter(["add", "list", "update", "delete", "back"], ignore_case=True)

    print("Students: 'add', 'list', 'update', 'delete' or 'back'.")
    while True:
        choice = prompt("Students > ", completer=commands).strip().lower()
        if choice == "add":
            cli_create_student()
        elif choice == "list":
            cli_list_students()
        elif choice == "update":
            cli_update_student()
        elif choice == "delete":
            cli_delete_student()
        elif choice == "back":
            break
        else:
            print("Unknown command.")

def cli_create_student() -> None:
    forename = ask_required_string("Forename")
    surname = ask_required_string("Surname")
    is_active = ask_required_bool("Is the student active? (yes/no) [yes]: ", default=True)

    with get_session() as session:
        parent_id = select_parent(session)
        if (parent_id is None):
            return

        parent = get_parent(session, parent_id)
        if not parent:
            print("No parent with that ID.")
            return
        
        created = create_student(session, data={
            "forename": forename,
            "surname": surname,
            "is_active": is_active,
            "parent_id": parent_id
        })

        if created:
            print(f"Created student: {created}")
        else:
            print("Failed to create student.")

def cli_list_students() -> None:
    try:
        with get_session() as session:
            students = list_students(session)
            if students:
                print_student_table(session)
            else:
                print("Zero students to list.")
    except Exception:
        print("Failed to retreive students.")

def cli_update_student() -> None:
    try:
        with get_session() as session:
            print_parents_with_students(session)

        student_id = ask_required_int("Enter ID of student to update")

        print("Leave blank to skip fields that should remain unchanged. ")
        forename = ask_optional_string("New forename")
        surname = ask_optional_string("New surname")
        is_active = ask_optional_bool("Is active (yes/no): ")
        with get_session() as session:
            parent_id = select_parent(session)
 
        updates = dict()
        if forename: updates["forename"] = forename
        if surname: updates["surname"] = surname
        if is_active is not None :updates["is_active"] = is_active
        if parent_id: updates["parent_id"] = parent_id

        with get_session() as session:
            if parent_id:
                parent = get_parent(session, parent_id)
                if not parent:
                    print("No parent with that ID.")
                    return
            updated = update_student(session, student_id, updates)
            if updated:
                print(f"Updated student: {updated}")
            else:
                print("Student not found.")

    except ValueError:
        print("Invalid input.")

def cli_delete_student() -> None:
    try:
        
        with get_session() as session: 
            print_parents_with_students(session)
            student_id = ask_required_int("Enter student ID to delete: ")
            student = get_student(session, student_id)
            if not student:
                print("Student not found.")
                return
            confirm = ask_required_bool(f"Are you sure you want to delete student {student.id} ({student.forename} {student.surname})? (yes/no): ", False)
            if confirm:
                if delete_student(session, student_id):
                    print("Successfully deleted student.")
                else:
                    print("Failed to delete student.")
            
    except ValueError:
        print("Invalid student ID.")


