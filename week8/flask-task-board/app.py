from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
DATA_FILE = Path(__file__).with_name("tasks.json")
STATUSES = {"todo", "doing", "done"}
PRIORITIES = {"low", "medium", "high"}


def load_tasks() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_tasks(tasks: list[dict]) -> None:
    DATA_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def normalize_form() -> tuple[dict, str]:
    title = request.form.get("title", "").strip()
    if not title:
        return {}, "Title is required."

    status = request.form.get("status", "todo")
    priority = request.form.get("priority", "medium")
    if status not in STATUSES:
        return {}, "Invalid status."
    if priority not in PRIORITIES:
        return {}, "Invalid priority."

    return {
        "title": title,
        "description": request.form.get("description", "").strip(),
        "status": status,
        "priority": priority,
    }, ""


@app.get("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks, form={}, editing=None, error="")


@app.post("/tasks")
def create_task():
    data, error = normalize_form()
    tasks = load_tasks()
    if error:
        return render_template("index.html", tasks=tasks, form=request.form, editing=None, error=error), 400

    tasks.insert(0, {"id": str(uuid.uuid4()), **data, "created_at": datetime.now(timezone.utc).isoformat()})
    save_tasks(tasks)
    return redirect(url_for("index"))


@app.get("/tasks/<task_id>/edit")
def edit_task(task_id: str):
    tasks = load_tasks()
    task = next((item for item in tasks if item["id"] == task_id), None)
    if not task:
        return redirect(url_for("index"))
    return render_template("index.html", tasks=tasks, form=task, editing=task_id, error="")


@app.post("/tasks/<task_id>")
def update_task(task_id: str):
    data, error = normalize_form()
    tasks = load_tasks()
    if error:
        return render_template("index.html", tasks=tasks, form=request.form, editing=task_id, error=error), 400

    for task in tasks:
        if task["id"] == task_id:
            task.update(data)
            task["updated_at"] = datetime.now(timezone.utc).isoformat()
            save_tasks(tasks)
            break
    return redirect(url_for("index"))


@app.post("/tasks/<task_id>/delete")
def delete_task(task_id: str):
    tasks = [task for task in load_tasks() if task["id"] != task_id]
    save_tasks(tasks)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5008)
