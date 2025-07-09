from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from db.cm import get_session
from services.student_service import create_student, list_students, get_student, update_student, delete_student
from services.parent_service import get_parent 

def handle_student_menu() -> None:
    commands = WordCompleter(["add", "list", "update", "delete", "back"], ignore_case=True)

    while True:
        choice = prompt("Students > ", completer=commands).strip().lower()
        
        if choice == "add":
            print("Adding student... (not yet implemented)")
        elif choice == "list":
            print("Listing students... (not yet implemented)")
        if choice == "update":
            print("Updating student... (not yet implemented)")
        elif choice == "delete":
            print("Deleting student... (not yet implemented)")
        elif choice == "back":
            break
        else:
            print("Unknown command.")

def cli_create_student() -> None:
    try:
        forename = prompt("Forename: ").strip()
        surname = prompt("Surname: ").strip()
        is_active = prompt("Is active, True or False (default True):  ").strip().lower()
        parent_id = int(prompt("Enter parent ID: "))

        if not forename or not surname or not (is_active in ["true", "false"]) or not parent_id:
            raise 

        with get_session() as db:
            parent = get_parent(db, parent_id)
            if not parent:
                print("No parent with that ID.")
                return
            
            created = create_student(db, data={"forename": forename, "surname": surname, "is_active": is_active == "true", "parent_id" : parent_id})
            if created:
                print(f"Created student: {created.id}")
            else:
                print("Failed to create student.")

    except ValueError:
        print("Invalid input.")

def cli_list_students() -> None:
    try:
        with get_session() as db:
            students = list_students(db)
            if students:
                for i in students:
                    print(i)
            else:
                raise Exception
    except Exception:
        print("Failed to retreive students.")

def cli_update_student() -> None:
    try:
        id = int(prompt("Enter ID of student to update: "))
        forename = prompt("New forename (leave blank to skip): ").strip()
        surname = prompt("New surname (leave blank to skip): ").strip()
        is_active = prompt("Is active, True or False (leave blank to skip): ").strip().lower()
        parent_id = int(prompt("New parent ID: (leave blank to skip): "))

        updates = dict()

        if forename:
            updates["forename"] = forename
        if surname:
            updates["surname"] = surname
        if is_active:
            updates["is_active"] = True if is_active == "true" else False
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
                print(f"Updated student: {updated.id}")
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
