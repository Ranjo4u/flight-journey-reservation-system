# Tests (CO7095)

## Automated (pytest)
Run from project root:
```bash
pip install pytest
pytest
```

Run one student's tests:
```bash
pytest tests/vrk5
```

Automated tests are under:
- `tests/*/whitebox/statement_coverage/*.py`
- `tests/*/whitebox/branch_coverage/*.py`
- `tests/*/whitebox/path_coverage/*.py`

## Manual / analytical (not executable)
- `tests/*/blackbox/**` (text-based test cases)
- `tests/*/whitebox/symbolic_execution/**` (path conditions + derived inputs)
- `tests/*/whitebox/concolic_testing/**` (mutated inputs + logs)
