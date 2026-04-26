# Week 5 Writeup

## Overview

In this assignment, I implemented two features using an AI-assisted workflow with Codex:

1. Pagination for list endpoints
2. Action item filters and bulk complete functionality

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

## AI Workflow (Codex)

I used Codex to:

* generate backend and frontend changes
* suggest API design
* implement tests
* debug environment issues

I guided Codex by:

* specifying features clearly
* limiting scope to minimal changes
* reviewing diffs before committing

## Key Learnings

* Pagination requires careful handling of offsets and limits
* Filtering queries in SQLAlchemy is straightforward once modeled correctly
* Bulk operations need error handling and rollback logic
* AI tools are effective when guided with precise instructions

## How to Run

```
cd week5
python -m pytest backend/tests
```

---
