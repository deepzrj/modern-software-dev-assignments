# Week 4 Writeup

## Overview

This assignment focuses on improving developer workflows using automation tools such as Claude custom commands, guidance files, and agent-based workflows. I implemented two automations that streamline testing and feature development within the starter FastAPI application.

---

# Automation 1: `/run-tests`

## Design Inspiration

Inspired by Claude Code best practices for repeatable workflows and fast feedback loops.

## Goal

Automate running backend tests and provide useful debugging feedback.

## Inputs

* Optional test path or marker

## Steps

1. Run:

   ```
   pytest -q backend/tests --maxfail=1 -x
   ```
2. If tests pass:

   * Run coverage analysis
3. If tests fail:

   * Identify failing tests
   * Summarize error messages
   * Suggest possible fixes

## Outputs

* Summary of test results
* Key error messages (if any)
* Suggested next steps

## How to Run

Use:

```
/run-tests
```

## Safety / Notes

* Stops on first failure for faster feedback
* Does not modify code
* Safe to run repeatedly

## Before vs After

**Before:**

* Manually run pytest
* Manually inspect errors
* Debug without guidance

**After:**

* One command runs tests
* Errors summarized automatically
* Suggested fixes improve efficiency

---

# Automation 2: `/dev-flow` (TestAgent + CodeAgent Workflow)

## Design Inspiration

Based on the SubAgents concept (TestAgent + CodeAgent collaboration).

## Goal

Automate feature development using a structured Test → Code → Verify workflow.

## Roles

### TestAgent

* Writes or updates tests in `backend/tests/`
* Ensures tests fail initially (test-first approach)

### CodeAgent

* Implements minimal code in `backend/app/`
* Fixes logic to pass tests

## Workflow

1. TestAgent creates a failing test
2. CodeAgent implements the feature
3. TestAgent runs tests:

   ```
   pytest -q backend/tests --maxfail=1 -x
   ```
4. If failing:

   * Summarize issues
   * Iterate
5. If passing:

   * Confirm success

## Outputs

* List of modified files
* Test results summary
* Remaining TODOs

## How to Run

Use:

```
/dev-flow <feature description>
```

## Safety / Notes

* Encourages minimal, reversible changes
* Prevents large, risky modifications
* Ensures correctness via testing

## Before vs After

**Before:**

* Write code first
* Add tests later (or skip)
* Debug inconsistently

**After:**

* Test-driven workflow
* Structured iteration
* Higher reliability and code quality

---

# How I Used the Automations

I used `/dev-flow` to guide feature development in the starter application. For example:

* Defined a new feature (e.g., adding or modifying an endpoint)
* Generated a failing test using the TestAgent approach
* Implemented the feature incrementally using CodeAgent logic
* Verified correctness using `/run-tests`

This significantly reduced debugging time and ensured correctness at each step.

Additionally, `/run-tests` was used repeatedly during development to quickly identify issues and validate fixes.

---

# Conclusion

These automations improved developer productivity by:

* Reducing repetitive manual testing
* Enforcing a structured development workflow
* Providing faster feedback and better debugging support

The combination of reusable commands and agent-based workflows makes the development process more efficient, reliable, and scalable.
