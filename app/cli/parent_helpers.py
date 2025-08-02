from sqlalchemy.orm import Session
from prompt_toolkit import prompt
from app.cli.cli_helpers import print_table
from app.models.parent import Parent
from app.services.parent_service import list_parents 

def select_parent(session: Session) -> int | None:
    parent_list = list_parents(session)
    if not parent_list:
        print("No parents available.")
        return None
    
    print("\nAvailable Parents:")
    print_parent_table(session)

    try:
        parent_id = int(prompt("Enter parent ID: ").strip())
        return parent_id
    except ValueError:
        print("Invalid input. Please enter a numeric parent ID.")
        return None
    
def format_name(p: Parent) -> str:
    return f"{p.forename} {p.surname}" 

def format_status(p: Parent) -> str:
    return "Active" if p.is_active else "Inactive"

def print_parent_table(session: Session) -> None:
    print_table(
        items=list_parents(session),
        columns=["id", "name", "status"],
        headers=["ID", "Name", "Status"],
        formatters={
            "name": format_name,
            "status": format_status,
        }
    )

