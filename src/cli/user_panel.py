from typing import Dict, Any

from src.cli.common_prompts import prompt_non_empty, prompt_optional, prompt_int
from src.services.flight_service import search_flights, list_all_flights
from src.services.booking_service import create_booking, list_bookings_for_user, cancel_booking, modify_booking_seat
from src.services.payment_service import pay_for_booking

def run_user_panel(session: Dict[str, Any]) -> None:
    email = session["email"]

    while True:
        print("\n=== USER PANEL ===")
        print("1. Search flights")
        print("2. View all flights")
        print("3. Create booking")
        print("4. Pay for booking")
        print("5. View my bookings")
        print("6. Cancel booking")
        print("7. Modify booking seat")
        print("0. Logout")

        choice = input("Select option: ").strip()

        if choice == "0":
            print("Logging out...")
            return

        if choice == "1":
            origin = prompt_non_empty("From (e.g., LHR): ").upper()
            dest = prompt_non_empty("To (e.g., JFK): ").upper()
            date_str = prompt_non_empty("Date (YYYY-MM-DD): ")
            airline = prompt_optional("Airline (optional): ").upper()
            max_price = prompt_int("Max base price (optional, press Enter for 999999): ", default=999999, min_value=1)
            ok, msg, results = search_flights(origin=origin, dest=dest, date_str=date_str, airline=airline, max_price=max_price)
            print(msg)
            for f in results:
                print(f"- {f['flight_id']} | {f['from']}->{f['to']} | {f['date']} | {f['airline']} | depart {f['depart']} | seats_left={f['seats_left']} | base_price={f['base_price']}")
            continue

        if choice == "2":
            flights = list_all_flights()
            if not flights:
                print("No flights available.")
            else:
                for f in flights:
                    print(f"- {f['flight_id']} | {f['from']}->{f['to']} | {f['date']} | {f['airline']} | depart {f['depart']} | arrive {f['arrive']} | seats_left={f['seats_left']} | base_price={f['base_price']}")
            continue

        if choice == "3":
            flight_id = prompt_non_empty("Flight ID: ").upper()
            passenger_name = prompt_non_empty("Passenger name: ")
            passengers = prompt_int("Number of passengers: ", min_value=1, max_value=9)
            seat_no = prompt_non_empty("Seat (e.g., 1A): ").upper()
            ok, msg, booking = create_booking(email=email, flight_id=flight_id, passenger_name=passenger_name, passengers=passengers, seat_no=seat_no)
            print(msg)
            if booking:
                print(f"Booking ID: {booking['booking_id']} | Amount: {booking['amount']} | Status: {booking['status']}")
            continue

        if choice == "4":
            booking_id = prompt_non_empty("Booking ID: ").strip()
            simulate = prompt_optional("Simulate outcome (blank/success, timeout, insufficient, fraud): ").strip().lower()
            ok, msg = pay_for_booking(email=email, booking_id=booking_id, simulate=simulate)
            print(msg)
            continue

        if choice == "5":
            bookings = list_bookings_for_user(email=email)
            if not bookings:
                print("No bookings found.")
            else:
                for b in bookings:
                    print(f"- {b['booking_id']} | flight={b['flight_id']} | seat={b['seat_no']} | passengers={b['passengers']} | amount={b['amount']} | status={b['status']}")
            continue

        if choice == "6":
            booking_id = prompt_non_empty("Booking ID to cancel: ").strip()
            ok, msg = cancel_booking(email=email, booking_id=booking_id)
            print(msg)
            continue

        if choice == "7":
            booking_id = prompt_non_empty("Booking ID: ").strip()
            new_seat = prompt_non_empty("New seat (e.g., 2B): ").upper()
            ok, msg = modify_booking_seat(email=email, booking_id=booking_id, new_seat_no=new_seat)
            print(msg)
            continue

        print("Invalid option. Try again.")
