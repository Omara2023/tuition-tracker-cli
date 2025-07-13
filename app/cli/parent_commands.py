from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from app.services.parent_service import create_parent, list_parents, update_parent, delete_parent, get_parent
from app.db.cm import get_session

def handle_parent_menu():
    commands = WordCompleter(["add", "list", "update", "delete", "back"], ignore_case=True)

    while True:
        choice = prompt("Parents > ", completer=commands).strip().lower()
        
        if choice == "add":
            cli_create_parent()
        elif choice == "list":
            cli_list_parents()
        elif choice == "update":
            cli_update_parent()
        elif choice == "delete":
            cli_delete_parent()
        elif choice == "back":
            break
        else:
            print("Unknown command.")

def cli_create_parent() -> None:
    try:
        forename = prompt("Forename: ").strip()
        surname = prompt("Surname: ").strip()
        is_active = prompt("Is active, yes or no (default yes): ").strip().lower()
    
        data = {}

        if not forename or not surname or not (is_active in ["yes", "y", "no", "n"]):
            raise ValueError

        data["forename"] = forename
        data["surname"] = surname
        data["is_active"] = is_active in ["yes" "y"]

        with get_session() as db:
            created = create_parent(db, data)
            if created:
                print(f"Created parent: {created}")
            else:
                print("Failed to create parent.")

    except ValueError:
        print("Invalid input.")

def cli_list_parents() -> None:
    try:
        with get_session() as db:
            parents = list_parents(db)
            if parents:
                for i in parents:
                    print(i)
            else:
                print("Failed to retrieve parents.")
    except Exception as e:
        print(f"Failed to retrieve parents {e}.")

def cli_update_parent() -> None:
    try:
        id = int(prompt("Enter parent ID to update: "))
        forename = prompt("New forename (leave blank to skip): ").strip()
        surname = prompt("New surname (leave blank to skip): ").strip()
        is_active = prompt("Is active, yes or no (leave blank to skip): ").strip().lower()

        updates = dict()

        if forename:
            updates["forename"] = forename
        if surname:
            updates["surname"] = surname
        if is_active:
            updates["is_active"] = True if is_active in ["yes", "y"] else False

        with get_session() as db:
            updated = update_parent(db, id, updates)
            if updated:
                print(f"Updated parent: {updated}")
            else:
                print("Parent not found.")

    except ValueError:
        print("Invalid input.")

def cli_delete_parent() -> None:
    try:
        id = int(prompt("Enter parent ID to delete: "))

        with get_session() as db: 
            to_delete = get_parent(db, id)
            if not to_delete:
                print(f"No parent exists with id {id}.")
                return
            choice = prompt(f"Are you sure you want to delete parent {to_delete.id} (yes or no)? ").strip().lower()
            if choice in ["y", "yes"]:
                if delete_parent(db, id):
                    print("Successfully deleted parent.")
                else:
                    print("Failed to delete parent.")
            
    except ValueError:
        print("Invalid parent id.")