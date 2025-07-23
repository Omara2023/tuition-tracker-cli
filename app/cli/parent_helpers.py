from sqlalchemy.orm import Session
from prompt_toolkit import prompt
from app.models.parent import Parent
from app.services.parent_service import list_parents 

def select_parent(session: Session) -> int | None:
    parent_list = list_parents(session)
    if not parent_list:
        print("No parents available.")
        return
    
    print("\nAvailable Parents:")
    print(f"{'ID':<5} {'Name':<20} {'Status':<10}")
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
    return f"{parent.id:<5} {full_name:<20} {status:<10}"
