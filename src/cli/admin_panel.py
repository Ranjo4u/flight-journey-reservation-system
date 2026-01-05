from typing import Dict, Any

from src.cli.common_prompts import prompt_non_empty, prompt_optional, prompt_int
from src.services.flight_service import admin_add_flight, admin_update_flight, admin_delete_flight, list_all_flights
from src.services.admin_report_service import report_all_bookings, report_revenue_summary, report_seat_utilisation, report_audit_summary

def run_admin_panel(session: Dict[str, Any]) -> None:
    while True:
        print("\n=== ADMIN PANEL ===")
        print("1. Add flight")
        print("2. Update flight")
        print("3. Delete flight")
        print("4. View all flights")
        print("5. View all bookings")
        print("6. Revenue summary")
        print("7. Seat utilisation report")
        print("8. Audit log summary")
        print("0. Logout")

        choice = input("Select option: ").strip()

        if choice == "0":
            print("Logging out...")
            return

        if choice == "1":
            flight_id = prompt_non_empty("Flight ID: ").upper()
            origin = prompt_non_empty("From (e.g., LHR): ").upper()
            dest = prompt_non_empty("To (e.g., JFK): ").upper()
            date_str = prompt_non_empty("Date (YYYY-MM-DD): ")
            airline = prompt_non_empty("Airline: ").upper()
            depart = prompt_non_empty("Depart (HH:MM): ")
            arrive = prompt_non_empty("Arrive (HH:MM): ")
            seats_total = prompt_int("Seats total: ", min_value=1, max_value=500)
            base_price = prompt_int("Base price: ", min_value=1, max_value=100000)

            ok, msg = admin_add_flight({
                "flight_id": flight_id,
                "from": origin,
                "to": dest,
                "date": date_str,
                "airline": airline,
                "depart": depart,
                "arrive": arrive,
                "seats_total": seats_total,
                "seats_left": seats_total,
                "base_price": base_price
            })
            print(msg)
            continue

        if choice == "2":
            flight_id = prompt_non_empty("Flight ID: ").upper()
            print("Enter fields to update (leave blank to skip).")
            patch = {}

            new_price = prompt_optional("New base price: ")
            if new_price.isdigit():
                patch["base_price"] = int(new_price)

            new_left = prompt_optional("New seats left: ")
            if new_left.isdigit():
                patch["seats_left"] = int(new_left)

            new_depart = prompt_optional("New depart time (HH:MM): ")
            if new_depart:
                patch["depart"] = new_depart

            new_arrive = prompt_optional("New arrive time (HH:MM): ")
            if new_arrive:
                patch["arrive"] = new_arrive

            new_airline = prompt_optional("New airline: ")
            if new_airline:
                patch["airline"] = new_airline.upper()

            if not patch:
                print("No updates provided.")
                continue

            ok, msg = admin_update_flight(flight_id=flight_id, patch=patch)
            print(msg)
            continue

        if choice == "3":
            flight_id = prompt_non_empty("Flight ID: ").upper()
            ok, msg = admin_delete_flight(flight_id=flight_id)
            print(msg)
            continue

        if choice == "4":
            flights = list_all_flights()
            if not flights:
                print("No flights available.")
            else:
                for f in flights:
                    print(f"- {f['flight_id']} | {f['from']}->{f['to']} | {f['date']} | {f['airline']} | depart {f['depart']} | seats_left={f['seats_left']} | base_price={f['base_price']}")
            continue

        if choice == "5":
            rows = report_all_bookings()
            if not rows:
                print("No bookings found.")
            else:
                for b in rows:
                    print(f"- {b['booking_id']} | {b['email']} | flight={b['flight_id']} | seat={b['seat_no']} | amount={b['amount']} | status={b['status']}")
            continue

        if choice == "6":
            print(report_revenue_summary())
            continue

        if choice == "7":
            print(report_seat_utilisation())
            continue

        if choice == "8":
            print(report_audit_summary())
            continue

        print("Invalid option. Try again.")
