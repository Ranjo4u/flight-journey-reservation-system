import json
import os
from typing import Any, Dict, List, Optional

class RepositoryError(Exception):
    pass

def _ensure_dir(path: str) -> None:
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)

def read_jsonl(path: str) -> List[Dict[str, Any]]:
    _ensure_dir(path)
    if not os.path.exists(path):
        return []
    rows: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict):
                    rows.append(obj)
            except json.JSONDecodeError:
                # Skip corrupted lines
                continue
    return rows

def append_jsonl(path: str, obj: Dict[str, Any]) -> None:
    _ensure_dir(path)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def overwrite_jsonl(path: str, rows: List[Dict[str, Any]]) -> None:
    _ensure_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def find_one(path: str, key: str, value: Any) -> Optional[Dict[str, Any]]:
    for r in read_jsonl(path):
        if r.get(key) == value:
            return r
    return None

def update_one(path: str, key: str, value: Any, patch: Dict[str, Any]) -> bool:
    rows = read_jsonl(path)
    updated = False
    for r in rows:
        if r.get(key) == value and not updated:
            r.update(patch)
            updated = True
    if updated:
        overwrite_jsonl(path, rows)
    return updated

def delete_one(path: str, key: str, value: Any) -> bool:
    rows = read_jsonl(path)
    before = len(rows)
    rows = [r for r in rows if r.get(key) != value]
    if len(rows) != before:
        overwrite_jsonl(path, rows)
        return True
    return False
