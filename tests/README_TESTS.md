# Tests (CO7095)

## Automated (pytest)
```bash
pip install pytest
pytest
```

Run one student:
```bash
pytest tests/vrk5
```

## Manual evidence
- Black-box: `tests/*/blackbox/**`
- Symbolic execution: `tests/*/whitebox/symbolic_execution/**`
- Concolic testing: `tests/*/whitebox/concolic_testing/**`
