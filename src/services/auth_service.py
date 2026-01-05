import hashlib
from typing import Dict, Optional, Tuple

from src.config import CONFIG
from src.constants import ROLE_ADMIN, ROLE_TRAVELLER
from src.persistence.jsonl_repository import append_jsonl, find_one, update_one
from src.persistence.audit_logger import log_event
from src.utils.validators import validate_email, validate_password

def _hash_password(password: str, salt: str) -> str:
    raw = (salt + password).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def register(email: str, password: str, role: str = ROLE_TRAVELLER) -> Tuple[bool, str]:
    ok, msg = validate_email(email)
    if not ok:
        return False, msg

    ok, msg = validate_password(password)
    if not ok:
        return False, msg

    email = email.strip().lower()
    role = role.strip().lower()
    if role not in (ROLE_TRAVELLER, ROLE_ADMIN):
        role = ROLE_TRAVELLER

    users_path = f"{CONFIG.data_dir}/{CONFIG.users_file}"
    if find_one(users_path, "email", email):
        return False, "User already exists."

    salt = hashlib.md5(email.encode("utf-8")).hexdigest()[:8]
    pw_hash = _hash_password(password, salt)

    append_jsonl(users_path, {
        "email": email,
        "role": role,
        "salt": salt,
        "pw_hash": pw_hash,
        "failed_attempts": 0,
        "locked": False
    })
    log_event("REGISTER", f"email={email} role={role}")
    return True, "Registration successful."

def login(email: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
    email = (email or "").strip().lower()
    users_path = f"{CONFIG.data_dir}/{CONFIG.users_file}"
    user = find_one(users_path, "email", email)
    if not user:
        log_event("LOGIN_FAIL_NOUSER", f"email={email}")
        return False, "User not found.", None

    if user.get("locked") is True:
        log_event("LOGIN_FAIL_LOCKED", f"email={email}")
        return False, "Account locked due to multiple failed attempts.", None

    salt = user.get("salt", "")
    expected = user.get("pw_hash", "")
    given = _hash_password(password or "", salt)

    if given == expected:
        update_one(users_path, "email", email, {"failed_attempts": 0, "locked": False})
        log_event("LOGIN_OK", f"email={email}")
        return True, "Login successful.", user

    attempts = int(user.get("failed_attempts", 0)) + 1
    patch = {"failed_attempts": attempts}
    if attempts >= 3:
        patch["locked"] = True
        log_event("LOGIN_FAIL_LOCK", f"email={email} attempts={attempts}")
        update_one(users_path, "email", email, patch)
        return False, "Too many failed attempts. Account locked.", None

    log_event("LOGIN_FAIL_BADPW", f"email={email} attempts={attempts}")
    update_one(users_path, "email", email, patch)
    return False, f"Invalid password. Attempts left: {3 - attempts}", None

def logout(email: str) -> None:
    if email:
        log_event("LOGOUT", f"email={email}")
