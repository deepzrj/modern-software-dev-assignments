# Warp Drive Prompt: Run Week 5 Tests

## Goal

Run the Week 5 backend test suite from the correct directory and summarize failures with the most likely file to inspect next.

## Prompt

From `week5/`, run:

```bash
PYTHONPATH=. pytest -q backend/tests --maxfail=1 -x
```

If the targeted run passes, run:

```bash
PYTHONPATH=. pytest -q backend/tests
```

Return a short report with:

- command run,
- pass/fail status,
- failing test and assertion if any,
- likely affected file,
- one concrete next step.

## Safety

This workflow is read-only. Do not edit files, install packages, or delete databases.
