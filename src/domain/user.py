from dataclasses import dataclass

@dataclass
class User:
    email: str
    role: str
    salt: str
    pw_hash: str
    failed_attempts: int = 0
    locked: bool = False
