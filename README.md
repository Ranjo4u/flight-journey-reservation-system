# Group7 Flight Journey Reservation System (CLI)

Python CLI backend-focused application for:
- User registration/login (traveller only)
- Admin login (seeded default admin)
- Flight CRUD (admin)
- Search flights, create booking, pay, cancel, modify seat (user)
- Text-based persistence via JSONL files under `data/`
- Audit logging under `data/audit.log`

## Run
```bash
python main.py
```

## Default Admin
- Email: admin@group7.com
- Password: Admin1234

## Dummy Users
- user1@demo.com .. user10@demo.com
- Password: User1234

## Tests
Automated white-box tests use pytest:
```bash
pip install pytest
pytest
```

Manual evidence:
- Black-box: `tests/*/blackbox/**`
- Symbolic execution: `tests/*/whitebox/symbolic_execution/**`
- Concolic testing: `tests/*/whitebox/concolic_testing/**`
