import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const STORAGE_KEY = "week8-bolt-task-board";
const emptyForm = { title: "", description: "", status: "todo", priority: "medium" };

function loadTasks() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function App() {
  const [tasks, setTasks] = useState(loadTasks);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
  }, [tasks]);

  const counts = useMemo(
    () => ({
      total: tasks.length,
      done: tasks.filter((task) => task.status === "done").length
    }),
    [tasks]
  );

  function updateField(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  function resetForm() {
    setForm(emptyForm);
    setEditingId(null);
    setError("");
  }

  function saveTask(event) {
    event.preventDefault();
    const title = form.title.trim();
    if (!title) {
      setError("Title is required.");
      return;
    }

    if (editingId) {
      setTasks((current) =>
        current.map((task) =>
          task.id === editingId
            ? { ...task, ...form, title, updatedAt: new Date().toISOString() }
            : task
        )
      );
    } else {
      setTasks((current) => [
        {
          id: crypto.randomUUID(),
          ...form,
          title,
          createdAt: new Date().toISOString()
        },
        ...current
      ]);
    }
    resetForm();
  }

  function editTask(task) {
    setForm({
      title: task.title,
      description: task.description,
      status: task.status,
      priority: task.priority
    });
    setEditingId(task.id);
    setError("");
  }

  function deleteTask(id) {
    setTasks((current) => current.filter((task) => task.id !== id));
    if (editingId === id) resetForm();
  }

  return (
    <main className="shell">
      <section className="header">
        <div>
          <p className="eyebrow">Week 8 / Bolt version</p>
          <h1>Task Board</h1>
        </div>
        <div className="stats">
          <span>{counts.total} tasks</span>
          <span>{counts.done} done</span>
        </div>
      </section>

      <section className="workspace">
        <form className="panel" onSubmit={saveTask}>
          <h2>{editingId ? "Edit task" : "New task"}</h2>
          {error && <p className="error">{error}</p>}
          <label>
            Title
            <input name="title" value={form.title} onChange={updateField} />
          </label>
          <label>
            Description
            <textarea name="description" value={form.description} onChange={updateField} rows="4" />
          </label>
          <div className="row">
            <label>
              Status
              <select name="status" value={form.status} onChange={updateField}>
                <option value="todo">Todo</option>
                <option value="doing">Doing</option>
                <option value="done">Done</option>
              </select>
            </label>
            <label>
              Priority
              <select name="priority" value={form.priority} onChange={updateField}>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </label>
          </div>
          <div className="actions">
            <button type="submit">{editingId ? "Save changes" : "Create task"}</button>
            {editingId && <button type="button" className="secondary" onClick={resetForm}>Cancel</button>}
          </div>
        </form>

        <section className="tasks" aria-label="Tasks">
          {tasks.length === 0 ? (
            <p className="empty">No tasks yet.</p>
          ) : (
            tasks.map((task) => (
              <article className="task" key={task.id}>
                <div>
                  <h3>{task.title}</h3>
                  <p>{task.description || "No description"}</p>
                </div>
                <div className="meta">
                  <span>{task.status}</span>
                  <span>{task.priority}</span>
                </div>
                <div className="taskActions">
                  <button type="button" onClick={() => editTask(task)}>Edit</button>
                  <button type="button" className="danger" onClick={() => deleteTask(task.id)}>Delete</button>
                </div>
              </article>
            ))
          )}
        </section>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
