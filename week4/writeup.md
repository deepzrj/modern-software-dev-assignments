# Week 4 Writeup

## Overview

This assignment focuses on improving developer workflows using Claude Code automations. I implemented two reusable command automations for the Week 4 FastAPI starter app:

- `week4/.claude/commands/run-tests.md`
- `week4/.claude/commands/dev-flow.md`

Together they create a repeatable test and feature-development workflow for the backend and frontend.

## Automation 1: `/run-tests`

Command file: `week4/.claude/commands/run-tests.md`

### Design Inspiration

This command follows the Claude Code best-practices idea of turning repeated terminal workflows into focused slash commands. The goal is fast, consistent feedback after code changes.

### Goal

Run Week 4 backend tests in a repeatable way and summarize failures with a concrete next debugging step.

### Inputs

`$ARGUMENTS` may be empty, a test file, or a specific pytest node.

Examples:

```text
/run-tests
/run-tests backend/tests/test_notes.py
/run-tests backend/tests/test_action_items.py::test_create_and_complete_action_item
```

### Steps

1. Confirm the command is being run from `week4/`.
2. Use `backend/tests` when no argument is provided.
3. Run targeted pytest with `--maxfail=1 -x`.
4. If targeted tests pass, run the full backend test suite.
5. If coverage tooling is available, run coverage for `backend/app`.
6. Summarize commands, pass/fail status, failing assertion, likely file, and next action.

### Expected Output

The command returns a concise test report:

- command run,
- status,
- failing test and traceback summary if any,
- likely file to inspect,
- next debugging step.

### Safety Notes

The command is read-only. It does not edit files, reset state, remove databases, or install packages.

### Before vs. After

Before, I manually remembered pytest commands and inspected raw tracebacks. After adding `/run-tests`, the workflow is documented in one place and produces a consistent test summary.

## Automation 2: `/dev-flow`

Command file: `week4/.claude/commands/dev-flow.md`

### Design Inspiration

This automation is based on the SubAgents pattern from the Claude Code documentation. Instead of creating separate persistent agent files, the command defines a reusable TestAgent -> CodeAgent -> Verify process inside one slash command.

### Goal

Guide small feature work through a scoped test-first workflow.

### Inputs

`$ARGUMENTS` should describe one feature or bug fix.

Example:

```text
/dev-flow add a case-insensitive notes search endpoint
```

### Workflow

1. Scope the requested behavior and identify likely files.
2. TestAgent phase: add or update the smallest useful test first.
3. CodeAgent phase: implement the minimum app change needed to pass the test.
4. Verify phase: run `pytest -q backend/tests --maxfail=1 -x`.
5. Final report: list behavior implemented, files changed, tests, verification result, and remaining risks.

### Expected Output

The command produces a short implementation report with:

- behavior implemented,
- changed files,
- tests added or updated,
- verification command and result,
- follow-up tasks if any.

### Safety Notes

The command explicitly limits work to the Week 4 app, avoids unrelated refactors, and warns against destructive database cleanup without approval.

### Before vs. After

Before, feature work could mix implementation, tests, and cleanup without a consistent order. After adding `/dev-flow`, small features follow a predictable loop: scope, test, implement, verify, report.

## How I Used the Automations to Enhance the Starter Application

I used the `/dev-flow` workflow to structure Week 4 app enhancements around tests and small changes. The command maps directly to the existing Week 4 app layout:

- routers in `backend/app/routers/`
- schemas in `backend/app/schemas.py`
- models in `backend/app/models.py`
- tests in `backend/tests/`
- frontend behavior in `frontend/app.js`

The workflow fits the implemented enhancements:

- `GET /notes/search/` is covered by `backend/tests/test_notes.py`.
- `PUT /action-items/{item_id}/complete` is covered by `backend/tests/test_action_items.py`.
- extraction behavior is covered by `backend/tests/test_extract.py`.

I used `/run-tests` as the verification step after these changes. The documented command runs the targeted pytest path first and then the full backend suite, which is the right feedback loop for this small FastAPI app.

## Conclusion

The two command files make the Week 4 developer workflow more repeatable:

- `/run-tests` standardizes verification.
- `/dev-flow` standardizes small feature implementation.

Both automations are checked into `week4/.claude/commands/` and are designed to be reused by Claude Code during future Week 4 development.

## Personal Learnings & Takeaways

Week 4 focused on turning repeated development steps into documented Claude Code commands. The two files in `week4/.claude/commands/` capture the exact test command, expected output format, and feature workflow boundaries for this app.

The `/run-tests` command is useful because it removes ambiguity about where tests should run and how failures should be summarized. The `/dev-flow` command is useful because it keeps small feature work scoped to a test, an implementation step, and verification.

I learned how to create reusable command sequences that:
- standardize repetitive tasks
- reduce manual errors
- improve consistency across development

The main takeaway was that process artifacts are most useful when they are specific to the repository: paths, commands, safety notes, and expected reports matter more than general workflow advice.
