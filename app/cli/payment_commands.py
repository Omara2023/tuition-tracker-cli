from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from datetime import datetime
from decimal import Decimal
from app.services.payment_service import create_payment, get_payment, update_payment, delete_payment
from app.services.parent_service import get_parent
from app.db.cm import get_session
from app.cli.cli_helpers import ask_required_int, ask_required_string, ask_required_float, ask_required_bool, ask_optional_int, ask_optional_float, ask_optional_string
from app.cli.parent_helpers import print_parent_table
from app.cli.payment_helpers import print_payments_with_parent

def handle_payment_menu():
    commands = WordCompleter(["add", "list", "update", "delete", "back"], ignore_case=True)

    print("Payments: 'add', 'list', 'update', 'delete' or 'back'.")
    while True:
        choice = prompt("Payments > ", completer=commands).strip().lower()
        
        if choice == "add":
            cli_create_payment()
        elif choice == "list":
            cli_list_payments()
        elif choice == "update":
            cli_update_payment()
        elif choice == "delete":
            cli_delete_payment()
        elif choice == "back":
            break
        else:
            print("Unknown command.")


def cli_create_payment() -> None:
    try:
        with get_session() as session:
            print_parent_table(session)
            parent_id = ask_required_int("Parent ID")
            timestamp = ask_required_string("Timestamp when payment was made")
            amount = ask_required_float("Payment amount (GBP)")
        
            data = {}

            data["parent_id"] = parent_id
            data["timestamp"] = datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
            data["amount"] = Decimal(str(amount))

            parent = get_parent(session, parent_id)
            if not parent:
                print("Invalid Parent ID.")
                return

            created = create_payment(session, data)
            if created:
                print(f"Created payment: {created}")
            else:
                print("Failed to create payment.")

            #--TODO: Implement "Would you like to link this payment to lessons?" workflow here.--#
    except ValueError:
        print("Invalid input.")

def cli_list_payments() -> None:
    try:
        with get_session() as session:
            print_payments_with_parent(session)
    except Exception as e:
        print(f"Failed to retrieve payments {e}.")

def cli_update_payment() -> None:
    try:
        id = ask_required_int("Payment ID of payment to update")
        parent_id = ask_optional_int("New ParentID (leave blank to skip)")
        timestamp = ask_optional_string("New payment time (leave blank to skip)")
        amount = ask_required_float("New amount (GBP) (leave blank to skip)")

        #--TODO: Implement workflow to change which lesson(s) a payment is linked to.--#
        updates = dict()

        if parent_id: updates["parent_id"] = parent_id
        if timestamp: updates["timestamp"] = timestamp
        if amount: updates["amount"] = Decimal(str(amount))

        with get_session() as db:
            updated = update_payment(db, id, updates)
            if updated:
                print(f"Updated payment: {updated}")
            else:
                print("Payment not found.")

    except ValueError:
        print("Invalid input.")

def cli_delete_payment() -> None:
    try:
        with get_session() as session: 
            print_payments_with_parent(session)
            id = ask_required_int("Enter Payment ID to delete")

            to_delete = get_payment(session, id)
            if not to_delete:
                print(f"No payment exists with id {id}.")
                return
            choice = ask_required_bool(f"Are you sure you want to delete payment {to_delete.id} (yes or no)? ")
            if choice:
                if delete_payment(session, id):
                    print("Successfully deleted payment.")
                else:
                    print("Failed to delete payment.")
            
    except ValueError:
        print("Invalid PaymentID.")