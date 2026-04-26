# /dev-flow

Run a reusable TestAgent -> CodeAgent -> Verify workflow for a small Week 4 feature or bug fix.

## Purpose

Use this command to make a scoped change to the Week 4 FastAPI app while keeping tests and implementation aligned. The workflow is intentionally narrow: one behavior change at a time.

## Input

`$ARGUMENTS` should describe the requested change, for example:

```text
add a case-insensitive notes search endpoint
```

If `$ARGUMENTS` is missing or too broad, ask one clarifying question before editing.

## Workflow

### 1. Scope

- Restate the requested behavior in one sentence.
- Identify likely files:
  - routers: `backend/app/routers/`
  - schemas: `backend/app/schemas.py`
  - models: `backend/app/models.py`
  - tests: `backend/tests/`
  - frontend: `frontend/app.js` and `frontend/index.html`
- Avoid unrelated refactors.

### 2. TestAgent Phase

- Add or update the smallest useful test first.
- Prefer endpoint tests in `backend/tests/test_notes.py` or `backend/tests/test_action_items.py`.
- For parser behavior, use `backend/tests/test_extract.py`.
- Run the targeted test and confirm it fails for the expected reason before implementation when practical.

### 3. CodeAgent Phase

- Implement the minimum code needed to satisfy the test.
- Follow existing FastAPI, SQLAlchemy, and Pydantic patterns in the Week 4 app.
- Keep API responses consistent with existing schemas.
- Do not change database schema unless the requested behavior requires it.

### 4. Verify Phase

Run:

```bash
pytest -q backend/tests --maxfail=1 -x
```

If tests fail, summarize the failing assertion, adjust the smallest relevant code path, and rerun the same command.

### 5. Final Report

Return:

- behavior implemented,
- files changed,
- tests added or updated,
- verification command and result,
- remaining risks or follow-up tasks.

## Rollback and Safety

- Do not touch Weeks 5-8.
- Do not rewrite unrelated files.
- Do not remove user changes.
- If the request requires destructive database cleanup, ask before running it.
