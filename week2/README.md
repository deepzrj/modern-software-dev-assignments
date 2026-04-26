# Week 2 - Action Item Extractor

Minimal FastAPI + SQLite app that turns free-form notes into action items. It includes the original rule-based extractor plus an Ollama-powered LLM extractor.

## Features

- Create and store notes in SQLite.
- Extract action items from pasted notes.
- Use `/action-items/extract` for deterministic rule-based extraction.
- Use `/action-items/extract-llm` for LLM-backed extraction through Ollama.
- Save extracted action items and mark them done from the frontend.
- Serve a simple static HTML frontend from the FastAPI app.

## Setup

From the repository root:

```bash
poetry install --no-interaction
```

For the LLM extractor, install Ollama and pull the model used by the app:

```bash
ollama run llama3.2:3b
```

The app uses SQLite at `week2/data/app.db`. The database tables are created automatically when the app starts.

## Run

From the repository root:

```bash
poetry run uvicorn week2.app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/
```

API docs are available at:

```text
http://127.0.0.1:8000/docs
```

## Test

From the repository root:

```bash
poetry run pytest week2/tests
```

The current tests cover the deterministic extraction logic. The LLM path requires a local Ollama runtime and should be tested with a mocked `ollama.chat` call for fully repeatable CI.

## API Endpoints

### Notes

- `POST /notes`
  - Body: `{ "content": "meeting notes" }`
  - Creates a saved note.

- `GET /notes/{note_id}`
  - Returns one saved note by ID.

### Action Items

- `POST /action-items/extract`
  - Body: `{ "text": "...", "save_note": true }`
  - Extracts action items with the rule-based extractor.

- `POST /action-items/extract-llm`
  - Body: `{ "text": "...", "save_note": true }`
  - Extracts action items with Ollama.
  - The model is prompted to return only a JSON array of strings.
  - If parsing fails, the implementation falls back to the rule-based extractor.

- `GET /action-items`
  - Lists saved action items.

- `POST /action-items/{action_item_id}/done`
  - Body: `{ "done": true }`
  - Marks an action item done or not done.

## Frontend Behavior

The Week 2 frontend is served at `/`. The main extraction button sends the note text to `/action-items/extract-llm`, optionally saves the note, renders returned action items, and updates item completion through `/action-items/{id}/done`.
