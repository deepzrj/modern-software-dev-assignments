# Bolt Task Board

React + Vite version of the Week 8 Task Board. This version represents the Bolt-generated stack and uses browser `localStorage` for persistence.

## Prerequisites

- Node.js 20+
- npm

## Setup

```bash
npm install
```

## Run

```bash
npm run dev
```

Open the local URL printed by Vite.

## Test

```bash
npm run build
```

Manual test:

1. Create a task.
2. Refresh the page and confirm it remains.
3. Edit the task status or priority.
4. Delete the task.
5. Try saving an empty title and confirm validation appears.

## Notes

- AI app generation platform: Bolt.new.
- Manual fixes after generation: kept the feature set small, stored data in `localStorage`, and simplified styling for a self-contained submission.
- Known issues: data is browser-local and not shared across devices.
