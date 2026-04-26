# /run-tests

Run the Week 4 backend test suite, summarize the result, and provide the next debugging step.

## Purpose

Use this command whenever a backend or frontend change may affect API behavior. It gives a repeatable test workflow for the Week 4 FastAPI app.

## Optional Arguments

`$ARGUMENTS` may be:

- empty: run the full backend test suite.
- a test file path, such as `backend/tests/test_notes.py`.
- a specific pytest node, such as `backend/tests/test_notes.py::test_create_and_list_notes`.

## Steps

1. Confirm the current directory is `week4/`. If not, explain that the command should be run from `week4/`.
2. Choose the test target:
   - If `$ARGUMENTS` is empty, use `backend/tests`.
   - Otherwise use `$ARGUMENTS` exactly as the pytest target.
3. Run:

   ```bash
   pytest -q <target> --maxfail=1 -x
   ```

4. If tests pass, run a broader verification:

   ```bash
   pytest -q backend/tests
   ```

5. If the full suite passes and coverage is available, run:

   ```bash
   pytest --cov=backend/app backend/tests
   ```

6. If any command fails:
   - identify the failing test name,
   - quote the relevant assertion or traceback line,
   - name the likely file to inspect,
   - recommend one concrete next action.

## Output Format

Return:

- command or commands run,
- pass/fail status,
- failing test and error summary if applicable,
- files likely involved,
- next step.

## Safety Notes

This command is read-only. It should not edit files, reset state, delete databases, or install packages unless the user explicitly asks.
