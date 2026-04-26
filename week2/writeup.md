# Week 2 Write-up

## Submission Details

Name: Student

SUNet ID: Not included in repository copy

Citations:
- Ollama structured outputs documentation: https://ollama.com/blog/structured-outputs
- FastAPI documentation: https://fastapi.tiangolo.com/

This assignment took me about 5 hours to do.

## Exercise 1: Scaffold a New Feature

Prompt:
```
Add an LLM-powered alternative to the existing rule-based action item extractor. Keep the existing heuristic extractor available, use Ollama for the new implementation, request a JSON array of strings from the model, and fall back to the rule-based extractor if the model output cannot be parsed.
```

Generated/Modified Code:
- `week2/app/services/extract.py`: added `extract_action_items_llm(text: str) -> List[str]`, an Ollama chat call using `llama3.2:3b`, a strict system prompt that asks for only a JSON array of strings, JSON parsing, code-fence cleanup, and fallback behavior.
- `week2/app/routers/action_items.py`: imported `extract_action_items_llm` so the backend can expose the LLM extractor through the API.

What changed:
The original `extract_action_items()` rule-based implementation remains intact. The new LLM path is additive and returns the same type, `List[str]`, so it can be used by the existing persistence flow.

## Exercise 2: Add Unit Tests

Prompt:
```
Add focused tests for the action item extraction logic. Cover bullet lists, checkboxes, numbered lists, keyword-style items, and normal narrative text that should not be extracted.
```

Generated/Modified Code:
- `week2/tests/test_extract.py`: includes a regression test for bullet, checkbox, and numbered-list parsing through the rule-based extractor.

What changed:
The current test file verifies the deterministic extractor. The LLM extractor depends on a local Ollama runtime, so it should be tested with a mock of `ollama.chat` before being used as a fully automated CI test.

## Exercise 3: Refactor Existing Code for Clarity

Prompt:
```
Clean up the backend so the database helpers, routers, and extraction service have clearer responsibilities. Keep the app minimal and avoid changing the public behavior unnecessarily.
```

Generated/Modified Code:
- `week2/app/db.py`: centralizes SQLite connection setup, table initialization, note insertion/listing, action item insertion/listing, and completion updates.
- `week2/app/main.py`: initializes the database, serves the frontend, mounts static files, and registers routers.
- `week2/app/routers/notes.py`: keeps note create and get-by-id behavior in the notes router.
- `week2/app/routers/action_items.py`: keeps extraction, LLM extraction, listing, and completion behavior in the action items router.
- `week2/app/services/extract.py`: separates rule-based extraction, LLM extraction, and imperative fallback detection.

What changed:
The backend now separates persistence, routing, and extraction logic. This keeps the app easier to inspect and makes the LLM extractor an isolated service-level feature.

## Exercise 4: Use Agentic Mode to Automate a Small Task

Prompt:
```
Wire the LLM extractor into the API and frontend. Add an endpoint for LLM extraction and update the UI so clicking the extraction button sends notes to the LLM-backed endpoint, saves the note when requested, renders returned action items, and lets users mark items done.
```

Generated/Modified Code:
- `week2/app/routers/action_items.py`: added `POST /action-items/extract-llm`, which validates text, optionally saves the note, extracts action items through `extract_action_items_llm`, stores the returned items, and returns IDs plus text.
- `week2/frontend/index.html`: the extraction button posts to `/action-items/extract-llm`, displays a loading state, renders returned action items, and sends completion updates to `/action-items/{id}/done`.
- `week2/app/db.py`: includes helpers used by the endpoint, including note insertion, action item insertion, listing, and done-state updates.

What changed:
The frontend now exercises the LLM extraction path directly. The checkbox behavior marks generated action items done after they are displayed.

## Exercise 5: Generate a README from the Codebase

Prompt:
```
Read the Week 2 FastAPI and frontend code and write a README that explains the app, setup, run commands, endpoints, tests, and the local Ollama dependency for LLM extraction.
```

Generated/Modified Code:
- `week2/README.md`: documents setup, running the app, testing, available features, API endpoints, and notes about Ollama.

What changed:
The Week 2 folder now includes a standalone README so the project can be run and evaluated without reading the assignment file first.

## Personal Learnings & Takeaways

Week 2 helped me connect LLM capabilities with a real backend system. Instead of just generating text, I was using the model to extract structured information and integrate it into an API.

I learned that LLM outputs are not always reliable, so testing and validation are important. I also got a better understanding of how frontend and backend components interact through API endpoints.

This week showed me how AI can be used as part of a complete system rather than as a standalone tool.

## Personal Learnings & Takeaways

Week 2 introduced the integration of LLMs into backend systems. The key concept here was **structured extraction**, where unstructured text is converted into structured data (e.g., JSON objects).

I worked with two approaches:
- **Rule-based extraction**: deterministic logic using string matching or patterns.
- **LLM-based extraction**: flexible extraction using natural language understanding.

The trade-off became clear: rule-based systems are predictable but brittle, while LLM-based systems are flexible but require validation.

I also learned about **API design**, where endpoints define contracts between frontend and backend. Each endpoint must clearly define inputs, outputs, and error handling.

The main takeaway was that LLM outputs must be treated as untrusted input and validated before being used in a system.
