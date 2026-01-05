from typing import Optional, Dict, Any

from src.services.auth_service import register, login, logout
from src.cli.user_panel import run_user_panel
from src.cli.admin_panel import run_admin_panel
from src.seed.seed_data import seed_if_empty
from src.constants import ROLE_ADMIN

def run_app() -> None:
    seed_if_empty()

    session: Optional[Dict[str, Any]] = None

    while True:
        print("\n=== Group7 Flight Journey Reservation System (CLI) ===")
        print("1. Register (traveller)")
        print("2. Login")
        print("0. Exit")
        choice = input("Select option: ").strip()

        if choice == "0":
            print("Goodbye.")
            return

        if choice == "1":
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            ok, msg = register(email=email, password=password)
            print(msg)
            continue

        if choice == "2":
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            ok, msg, user = login(email=email, password=password)
            print(msg)
            if not ok or not user:
                continue

            session = {"email": user["email"], "role": user["role"]}
            if session["role"] == ROLE_ADMIN:
                run_admin_panel(session)
            else:
                run_user_panel(session)

            logout(session["email"])
            session = None
            continue

        print("Invalid option. Try again.")
