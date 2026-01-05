from typing import Dict, Tuple

from src.config import CONFIG
from src.persistence.jsonl_repository import append_jsonl
from src.persistence.audit_logger import log_event
from src.utils.id_generator import generate_payment_id
from src.services.booking_service import get_booking, mark_paid

def _payments_path() -> str:
    return f"{CONFIG.data_dir}/{CONFIG.payments_file}"

def validate_card(card_number: str, expiry_mm_yy: str, cvv: str) -> Tuple[bool, str]:
    card_number = (card_number or "").replace(" ", "")
    expiry_mm_yy = (expiry_mm_yy or "").strip()
    cvv = (cvv or "").strip()

    if not card_number.isdigit():
        return False, "Card number must be digits only."
    if len(card_number) not in (13, 15, 16):
        return False, "Card number length invalid."
    if not cvv.isdigit() or len(cvv) not in (3, 4):
        return False, "CVV invalid."

    parts = expiry_mm_yy.split("/")
    if len(parts) != 2:
        return False, "Expiry must be MM/YY."
    mm, yy = parts
    if not (mm.isdigit() and yy.isdigit()):
        return False, "Expiry must be numeric MM/YY."
    m = int(mm)
    if m < 1 or m > 12:
        return False, "Expiry month out of range."

    # Simple expiry check (branch-friendly)
    # Not using system date here to keep deterministic tests possible
    if int(yy) < 24:
        return False, "Card expired (YY < 24)."

    return True, "Card valid."

def process_payment(amount: int, simulate: str = "") -> Tuple[bool, str, Dict]:
    if amount <= 0:
        return False, "Amount must be positive.", {"status": "FAILED", "reason": "AMOUNT"}

    simulate = (simulate or "").strip().lower()
    if simulate == "timeout":
        return False, "Payment timeout.", {"status": "FAILED", "reason": "TIMEOUT"}
    if simulate == "insufficient":
        return False, "Insufficient funds.", {"status": "FAILED", "reason": "FUNDS"}
    if simulate == "fraud":
        return False, "Payment flagged as suspicious.", {"status": "FAILED", "reason": "FRAUD"}

    return True, "Payment successful.", {"status": "SUCCESS", "amount": amount}

def pay_for_booking(email: str, booking_id: str, simulate: str = "") -> Tuple[bool, str]:
    email = (email or "").strip().lower()
    booking = get_booking(booking_id)
    if not booking:
        return False, "Booking not found."
    if booking.get("email") != email:
        return False, "You can only pay for your own booking."
    if booking.get("status") == "PAID":
        return False, "Booking is already PAID."
    if booking.get("status") == "CANCELLED":
        return False, "Cannot pay for a cancelled booking."

    amount = int(booking.get("amount", 0))
    ok, msg, details = process_payment(amount=amount, simulate=simulate)
    payment_id = generate_payment_id(booking_id)

    payment_row = {
        "payment_id": payment_id,
        "booking_id": booking_id,
        "email": email,
        "amount": amount,
        "status": details.get("status", "FAILED"),
        "reason": details.get("reason", "")
    }
    append_jsonl(_payments_path(), payment_row)

    if ok:
        mark_paid(booking_id)
        log_event("PAYMENT_OK", f"payment_id={payment_id} booking_id={booking_id} amount={amount}")
        return True, f"Payment successful. Booking marked as PAID. Payment ID: {payment_id}"

    log_event("PAYMENT_FAIL", f"payment_id={payment_id} booking_id={booking_id} reason={payment_row['reason']}")
    return False, f"Payment failed: {msg}. Payment ID: {payment_id}"
