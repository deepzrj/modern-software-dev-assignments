# Flask Task Board

Python Flask version of the Week 8 Task Board. Tasks are persisted to `tasks.json`.

## Prerequisites

- Python 3.11+
- Flask

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install flask
```

On macOS/Linux, activate with `source .venv/bin/activate`.

Alternatively:

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Open `http://127.0.0.1:5008`.

## Test

```bash
python -m py_compile app.py
```

Manual test:

1. Create a task.
2. Stop and restart the server and confirm the task remains.
3. Edit the task.
4. Delete the task.
5. Submit an empty title and confirm validation appears.

## Notes

- AI app generation platform: none; implemented manually.
- Manual fixes after generation: not applicable.
- Known issues: persistence is a local JSON file and has no multi-user locking.
