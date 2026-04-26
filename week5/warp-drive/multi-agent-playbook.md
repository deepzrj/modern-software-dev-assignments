# Warp Multi-Agent Playbook

## Goal

Coordinate independent agents in separate Warp tabs for Week 5 feature work without overlapping edits.

## Agent Roles

- Backend API Agent: owns `backend/app/routers/`, `backend/app/schemas.py`, and backend tests.
- Frontend Agent: owns `frontend/index.html`, `frontend/app.js`, and `frontend/styles.css`.
- Verification Agent: runs tests and reviews diffs after the other agents finish.

## Workflow Used

1. Backend API Agent implemented pagination for notes/action-items and bulk complete behavior.
2. Frontend Agent wired pagination controls, action item filters, and selected-item bulk completion.
3. Verification Agent ran `PYTHONPATH=. pytest -q backend/tests`, checked endpoint contracts, and reported remaining risks.

## Coordination Rules

- Each agent owns a disjoint file set.
- Agents do not rewrite files outside `week5/`.
- Verification runs after implementation agents finish.
- If two agents need the same file, pause and assign one owner before editing.
