from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from sqlalchemy.orm import Session
from app.services.parent_service import create_parent, list_parents, update_parent, delete_parent, get_parent
from app.cli.cli_helpers import ask_required_string, ask_required_bool, ask_optional_bool, ask_optional_string
from app.cli.parent_helpers import print_parent_table, select_parent
from app.models.parent import Parent
from app.db.cm import get_session

def handle_parent_menu():
    commands = WordCompleter(["add", "list", "update", "delete", "back"], ignore_case=True)

    print("Parents: 'add', 'list', 'update', 'delete' or 'back'.")
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
        forename = ask_required_string("Forename")
        surname = ask_required_string("Surname")
        is_active = ask_required_bool("Is the parent active? (yes/no) [yes]: ", default=True)
    
        data = {"forename": forename, "surname": surname, "is_active": is_active}

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
        with get_session() as session:
            parents = list_parents(session)
            if parents:
                print_parent_table(session)
            else:
                print("Failed to retrieve parents.")
    except Exception as e:
        print(f"Failed to retrieve parents {e}.")

def cli_update_parent() -> None:
    try:
        with get_session() as session:
            parent = _cli_parent_selection(session)
            if parent is None: 
                return
            else:
                parent_id = parent.id
        forename = ask_optional_string("New forename")
        surname = ask_optional_string("New surname")
        is_active = ask_optional_bool("Is active, yes or no (leave blank to skip): ")

        updates = dict()
        if forename: updates["forename"] = forename
        if surname: updates["surname"] = surname
        if is_active: updates["is_active"] = is_active

        with get_session() as db:
            updated = update_parent(db, parent_id, updates)
            print(f"Updated parent: {updated}")
            
    except ValueError:
        print("Invalid input.")

def cli_delete_parent() -> None:
    try:
        with get_session() as db:
            parent = _cli_parent_selection(db)
            if parent is None: return
            choice = ask_required_bool(f"Are you sure you want to delete parent {parent.id} (yes or no)?", default=False)
            if choice:
                parent_id = parent.id
                if delete_parent(db, parent_id):
                    print("Successfully deleted parent.")
                else:
                    print("Failed to delete parent.")
            
    except ValueError:
        print("Invalid parent id.")

def _cli_parent_selection(session: Session) -> Parent | None:
    parent_id = select_parent(session)
    if parent_id is None:
        return None
    parent = get_parent(session, parent_id)
    if not parent:
        print(f"No parent exists with id {parent_id}.")
        return None
    return parent