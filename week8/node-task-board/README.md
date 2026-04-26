# Node Task Board

Node.js version of the Week 8 Task Board. It uses the built-in `http` module for the backend, vanilla JavaScript for the frontend, and `tasks.json` for persistence.

## Prerequisites

- Node.js 20+

## Setup

No package installation is required.

## Run

```bash
npm start
```

Open `http://127.0.0.1:5009`.

## Test

```bash
node --check server.js
node --check public/app.js
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
