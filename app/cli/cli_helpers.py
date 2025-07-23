from prompt_toolkit import prompt

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

