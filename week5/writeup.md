# Week 5 Writeup

## Overview

In this assignment, I implemented two Week 5 tasks using a Warp-style agentic workflow:

1. Pagination for list endpoints
2. Action item filters and bulk complete functionality

The workflow artifacts are checked in under `week5/warp-drive/`:

- `warp-drive/run-week5-tests.md`
- `warp-drive/multi-agent-playbook.md`

## Features Implemented

### 1. Pagination

* Added pagination to notes and action items endpoints
* Supported query parameters:

  * `page`
  * `page_size`
* Updated backend queries to return paginated results
* Updated frontend to support page navigation (Prev/Next)

### 2. Action Item Filters + Bulk Complete

* Added filtering by:

  * completed
  * open
* Added endpoint:

  * `POST /action-items/bulk-complete`
* Implemented bulk update logic with rollback behavior
* Updated frontend with:

  * filter dropdown
  * “Complete selected” button

## Testing

* Added backend tests for:

  * pagination behavior
  * filtering logic
  * bulk completion
* All tests pass:

```
python -m pytest backend/tests
```

## Warp Drive Automation

I created a reusable Warp Drive prompt in `warp-drive/run-week5-tests.md`.

Goal:

* run Week 5 tests from the correct directory
* preserve the required `PYTHONPATH=.`
* summarize failures and next debugging steps

Before this prompt, I manually remembered the exact test command and parsed raw pytest output. Afterward, the verification workflow is repeatable and easy to invoke from Warp.

## Warp Multi-Agent Workflow

I documented the multi-agent workflow in `warp-drive/multi-agent-playbook.md`.

Agent roles:

* Backend API Agent owned routers, schemas, and backend tests.
* Frontend Agent owned the static frontend files.
* Verification Agent owned test execution and final review.

Coordination strategy:

* agents worked on disjoint file sets
* implementation stayed inside `week5/`
* verification ran after the feature agents completed

Concurrency wins:

* backend pagination/filtering and frontend wiring could proceed independently once the API contract was agreed on
* test verification was separated from implementation, which made it easier to catch contract drift

Risks:

* frontend and backend agents can diverge if endpoint response shapes are not written down first
* shared files such as schemas need a single clear owner

## Key Learnings

* Pagination requires careful handling of offsets and limits
* Filtering queries in SQLAlchemy is straightforward once modeled correctly
* Bulk operations need error handling and rollback logic
* AI tools are effective when guided with precise instructions

## How to Run

```
cd week5
PYTHONPATH=. pytest -q backend/tests
```

## Personal Learnings & Takeaways

Week 5 gave me more practice splitting feature work across backend, frontend, and verification responsibilities. Pagination and filtering required the API response shape to be written down first so the frontend controls could match the backend behavior.

I worked on these concepts:
- **Pagination**: splitting large datasets into smaller pages using parameters like page and page_size
- **Filtering**: selecting subsets of data based on conditions
- **Bulk operations**: applying actions to multiple items at once

The multi-agent playbook helped identify a practical risk: shared files such as schemas need one owner, or concurrent agents can make incompatible assumptions. The verification role is also important because passing backend tests does not automatically prove the frontend is using the same contract.

The main takeaway was that agentic workflows need clear file ownership, endpoint contracts, and a final verification pass.
