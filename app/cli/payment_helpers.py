from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.payment import Payment
from app.models.parent import Parent
from app.cli.cli_helpers import print_join_table

def print_payments_with_parent(session: Session) -> None:
    items = session.execute(select(Parent, Payment).join(Parent.payments)).all()
    if items is None:
        print("No payments to print.")
        return 
    
    print_join_table(
        rows=items,
        columns=[
            lambda t: t[1].id,
            lambda t: f"{t[0].forename} {t[0].surname}",
            lambda t: t[1].amount,
            lambda t: str(t[1].timestamp)
        ],
        headers=["Payment ID", "Parent", "Amount", "Date"]
    )