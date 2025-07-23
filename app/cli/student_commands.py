from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from sqlalchemy.orm import Session
from app.db.cm import get_session
from app.services.student_service import create_student, list_students, get_student, update_student, delete_student
from app.services.parent_service import get_parent, list_parents 
from app.cli.cli_helpers import ask_bool, ask_required_string
from app.models.parent import Parent

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
    is_active = ask_bool("Is the student active? (yes/no) [yes]: ", default=True)

    with get_session() as db:
        parent_id = select_parent(db)
        if (parent_id is None):
            return

        parent = get_parent(db, parent_id)
        if not parent:
            print("No parent with that ID.")
            return
        
        created = create_student(db, data={
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
        with get_session() as db:
            students = list_students(db)
            if students:
                for i in students:
                    print(i)
            else:
                print("Zero students to list.")
    except Exception:
        print("Failed to retreive students.")

def cli_update_student() -> None:
    try:
        id = int(prompt("Enter ID of student to update: "))
        forename = prompt("New forename (leave blank to skip): ").strip()
        surname = prompt("New surname (leave blank to skip): ").strip()
        is_active = prompt("Is active, yes or no (leave blank to skip): ").strip().lower()
        parent_id = int(prompt("New parent ID: (leave blank to skip): "))

        updates = dict()

        if forename:
            updates["forename"] = forename
        if surname:
            updates["surname"] = surname
        if is_active:
            updates["is_active"] = True if is_active in ["yes", "y"] else False
        if parent_id:
            updates["parent_id"] = parent_id

        with get_session() as db:
            if parent_id:
                parent = get_parent(db, parent_id)
                if not parent:
                    print("No parent with that ID.")
                    return
            updated = update_student(db, id, updates)
            if updated:
                print(f"Updated student: {updated}")
            else:
                print("Student not found.")

    except ValueError:
        print("Invalid input.")

def cli_delete_student() -> None:
    try:
        id = int(prompt("Enter parent ID to delete: "))

        with get_session() as db: 
            to_delete = get_student(db, id)
            choice = prompt(f"Are you sure you want to delete student {to_delete.id} (yes or no)?").strip().lower()
            if choice in ["y", "yes"]:
                if delete_student(db, id):
                    print("Successfully deleted student.")
                else:
                    print("Failed to delete student.")
            
    except ValueError:
        print("Invalid student id.")

def select_parent(session: Session) -> int | None:
    parent_list = list_parents(session)
    if not parent_list:
        print("No parents available.")
        return
    
    print("\nAvailable Parents:")
    print(f"{'ID':<5} {'Name':<25} {'Status'}")
    for parent in parent_list:
        print(format_parent_row(parent))
    print()

    try:
        parent_id = int(prompt("Enter parent ID: ").strip())
        return parent_id
    except ValueError:
        print("Invalid input. Please enter a numeric parent ID.")
        return None
    
def format_parent_row(parent: Parent) -> str:
    status = "Active" if bool(parent.is_active) else "Inactive"
    full_name = f"{parent.forename} {parent.surname}"
    return f"{parent.id:<5} {full_name:<25} {status}"

def format_student_row(student) -> str:
    full_name = f"{student.forename} {student.surname}"
    status = "Active" if student.is_active else "Inactive"
    return f"{student.id:<5} {full_name:<25} {status:<10} Parent ID: {student.parent_id}"

