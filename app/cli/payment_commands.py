from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from datetime import datetime
from app.services.payment_service import create_payment, list_payments, get_payment, update_payment, delete_payment
from app.services.parent_service import get_parent
from app.db.cm import get_session

def handle_payment_menu():
    commands = WordCompleter(["add", "list", "update", "delete", "back"], ignore_case=True)

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
        parent_id = int(prompt("ParentID of payment maker: ").strip())
        timestamp = prompt("Timestamp when payment was made: ").strip()
        amount = prompt("Payment amount (GBP): ").strip().lower()
    
        data = {}

        if not parent_id or not timestamp or not amount:
            raise ValueError

        data["parent_id"] = parent_id
        data["timestamp"] = datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
        data["amount"] = float(amount)

        with get_session() as db:
            parent = get_parent(db, parent_id)
            if not parent:
                print("Invalid ParentID.")
                return

            created = create_payment(db, data)
            if created:
                print(f"Created payment: {created}")
            else:
                print("Failed to create payment.")

            #--TODO: Implement "Would you like to link this payment to lessons?" workflow here.--#
    except ValueError:
        print("Invalid input.")

def cli_list_payments() -> None:
    try:
        with get_session() as db:
            if (payments := list_payments(db)) :
                for i in payments:
                    print(i)
            else:
                print("Failed to retrieve payments.")
    except Exception as e:
        print(f"Failed to retrieve payments {e}.")

def cli_update_payment() -> None:
    try:
        id = int(prompt("Enter PaymentID to update: "))
        parent_id = prompt("New ParentID (leave blank to skip): ").strip()
        timestamp = prompt("New payment time (leave blank to skip): ").strip()
        amount = prompt("New amount (GBP) (leave blank to skip): ").strip().lower()

        #--TODO: Implement workflow to change which lesson(s) a payment is linked to.--#
        updates = dict()

        if parent_id:
            updates["parent_id"] = int(parent_id)
        if timestamp:
            updates["timestamp"] = timestamp
        if amount:
            updates["amount"] = float(amount)

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
        id = int(prompt("Enter PaymentID to delete: "))

        with get_session() as db: 
            to_delete = get_payment(db, id)
            if not to_delete:
                print(f"No payment exists with id {id}.")
                return
            choice = prompt(f"Are you sure you want to delete payment {to_delete.id} (yes or no)? ").strip().lower()
            if choice in ["y", "yes"]:
                if delete_payment(db, id):
                    print("Successfully deleted payment.")
                else:
                    print("Failed to delete payment.")
            
    except ValueError:
        print("Invalid PaymentID.")