from typing import Optional

def prompt_non_empty(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("Value cannot be empty. Try again.")

def prompt_optional(prompt: str) -> str:
    return input(prompt).strip()

def prompt_int(prompt: str, default: Optional[int] = None, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        if not raw.isdigit():
            print("Please enter a valid number.")
            continue
        val = int(raw)
        if min_value is not None and val < min_value:
            print(f"Value must be >= {min_value}.")
            continue
        if max_value is not None and val > max_value:
            print(f"Value must be <= {max_value}.")
            continue
        return val
