from prompt_toolkit import prompt
from collections.abc import Sequence, Callable
from sqlalchemy.engine import Row

def ask_required_string(field_name: str) -> str:
    while True:
        value = prompt(f"{field_name}: ").strip()
        if value:
            return value
        print(f"{field_name} is required.")

def ask_optional_string(field_name: str) -> str | None:
    value = prompt(f"{field_name} (leave blank to skip): ").strip()
    return value or None

def ask_required_int(field_name: str) -> int:
    while True:
        raw = prompt(f"{field_name} (number required): ").strip()
        try:
            return int(raw)
        except ValueError:
            print("Invalid input. Must be a number.")

def ask_optional_int(field_name: str) -> int | None:
    raw = prompt(f"{field_name} (leave blank to skip): ").strip()
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        print("Invalid input. Must be a number.")
        return None

def ask_required_bool(prompt_text: str, default: bool = True) -> bool:
    raw = prompt(f"{prompt_text} [{'yes' if default else 'no'}]: ").strip().lower()
    if raw in ["yes", "y"]: return True
    if raw in ["no", "n"]: return False
    return default

def ask_optional_bool(prompt_text: str, default: bool | None = None) -> bool | None:
    while True:
        prompt_label = f"{prompt_text}" + (f" [default: {'yes' if default else 'no'}]" if default is not None else "")
        raw = prompt(f"{prompt_label}: ").strip().lower()
        
        if not raw:
            return default 
        if raw in ["yes", "y"]:
            return True
        if raw in ["no", "n"]:
            return False

        print("Invalid input. Please enter 'yes' or 'no', or leave blank.")

def print_model_table(items, columns: list[str], headers: list[str] | None = None, formatters: dict | None = None):
    """
    Print a formatted table of objects to the console.

    Parameters:
    - items (list): A list of objects to display as rows. Each object should have
      attributes corresponding to the specified columns.
    - columns (list[str]): List of attribute names or keys to extract from each item.
      These identify which data to show in each column.
    - headers (list[str] | None): Optional list of column header names to print.
      If None, the `columns` list is used as headers.
    - formatters (dict | None): Optional dictionary mapping column names to functions
      that take an item and return a string to display for that column.
      Use this for computed or combined columns (e.g., concatenating first and last name).

    Behavior:
    - Dynamically calculates column widths based on header names and cell content.
    - Prints a header row with column names, a separator line, and one row per item.
    - Adds a blank line before and after the table for readability.
    - Prints a friendly message and returns early if `items` is empty or None.

    Example usage:

        def format_name(p):
            return f"{p.forename} {p.surname}"

        def format_status(p):
            return "Active" if p.is_active else "Inactive"

        print_table(
            parent_list,
            columns=["id", "name", "status"],
            headers=["ID", "Name", "Status"],
            formatters={"name": format_name, "status": format_status}
        )
    """
    if not items:
        print("No data to display.")
        return
    
    headers = headers or columns
    formatters = formatters or {}

    widths = []
    for column, header in zip(columns, headers):
        max_width = len(header)
        for item in items:
            val = formatters[column](item) if column in formatters else getattr(item, column, "")
            max_width = max(max_width, len(str(val)))
        widths.append(max_width)

    #Header and separator:
    print(" | ".join(f"{h:<{w}}" for h, w in zip(headers, widths)))
    print("-+-".join("-" * w for w in widths))

    #Print rows:

    for item in items:
        row = []
        for column, width in zip(columns, widths):
            val = formatters[column](item) if column in formatters else getattr(item, column, "")
            row.append(f"{val:<{width}}")
        print(" | ".join(row))
    print()


def print_join_table(rows: Sequence[Row], columns: list[Callable[[Row], str]], headers: list[str]) -> None:
    """Pretty-print rows of joined ORM objects using extractor functions."""
    if not rows:
        print("No data to display")
        return
    
    #Column width calculator:
    widths = []
    for i, header in enumerate(headers):
        max_width = len(header)
        for row in rows:
            val = str(columns[i](row))
            max_width = max(max_width, len(val))
        widths.append(max_width)

    #Print header:
    print(" | ".join(f"{h:<{w}}" for h, w in zip(headers, widths)))
    print("-+-".join("-" * w for w in widths))

    #Rows:
    for row in rows:
        row = [f"{columns[i](row):<{widths[i]}}" for i in range(len(headers))]
        print(" | ".join(row))
    print()