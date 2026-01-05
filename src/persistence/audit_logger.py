import time
from typing import Optional
from src.config import CONFIG

def log_event(event: str, extra: Optional[str] = None) -> None:
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} | {event}"
    if extra:
        line += f" | {extra}"
    path = f"{CONFIG.data_dir}/{CONFIG.audit_file}"
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
