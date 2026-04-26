const form = document.querySelector("#taskForm");
const fields = {
  id: document.querySelector("#taskId"),
  title: document.querySelector("#title"),
  description: document.querySelector("#description"),
  status: document.querySelector("#status"),
  priority: document.querySelector("#priority")
};
const tasksEl = document.querySelector("#tasks");
const countEl = document.querySelector("#count");
const errorEl = document.querySelector("#error");
const formTitleEl = document.querySelector("#formTitle");
const submitButton = document.querySelector("#submitButton");
const cancelButton = document.querySelector("#cancelButton");

let tasks = [];

function taskPayload() {
  return {
    title: fields.title.value,
    description: fields.description.value,
    status: fields.status.value,
    priority: fields.priority.value
  };
}

function setError(message) {
  errorEl.textContent = message;
  errorEl.hidden = !message;
}

function resetForm() {
  form.reset();
  fields.id.value = "";
  fields.priority.value = "medium";
  formTitleEl.textContent = "New task";
  submitButton.textContent = "Create task";
  cancelButton.hidden = true;
  setError("");
}

function render() {
  countEl.textContent = `${tasks.length} ${tasks.length === 1 ? "task" : "tasks"}`;
  if (!tasks.length) {
    tasksEl.innerHTML = `<p class="empty">No tasks yet.</p>`;
    return;
  }

  tasksEl.innerHTML = tasks
    .map(
      (task) => `
        <article class="task">
          <div>
            <h3>${escapeHtml(task.title)}</h3>
            <p>${escapeHtml(task.description || "No description")}</p>
          </div>
          <div class="meta">
            <span>${escapeHtml(task.status)}</span>
            <span>${escapeHtml(task.priority)}</span>
          </div>
          <div class="actions">
            <button type="button" data-edit="${task.id}">Edit</button>
            <button type="button" class="danger" data-delete="${task.id}">Delete</button>
          </div>
        </article>
      `
    )
    .join("");
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;"
  })[char]);
}

async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Request failed.");
  return data;
}

async function loadTasks() {
  tasks = await request("/api/tasks");
  render();
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const id = fields.id.value;
  try {
    if (id) {
      const updated = await request(`/api/tasks/${id}`, {
        method: "PUT",
        body: JSON.stringify(taskPayload())
      });
      tasks = tasks.map((task) => (task.id === id ? updated : task));
    } else {
      const created = await request("/api/tasks", {
        method: "POST",
        body: JSON.stringify(taskPayload())
      });
      tasks = [created, ...tasks];
    }
    resetForm();
    render();
  } catch (error) {
    setError(error.message);
  }
});

tasksEl.addEventListener("click", async (event) => {
  const editId = event.target.dataset.edit;
  const deleteId = event.target.dataset.delete;

  if (editId) {
    const task = tasks.find((item) => item.id === editId);
    fields.id.value = task.id;
    fields.title.value = task.title;
    fields.description.value = task.description;
    fields.status.value = task.status;
    fields.priority.value = task.priority;
    formTitleEl.textContent = "Edit task";
    submitButton.textContent = "Save changes";
    cancelButton.hidden = false;
  }

  if (deleteId) {
    await request(`/api/tasks/${deleteId}`, { method: "DELETE" });
    tasks = tasks.filter((task) => task.id !== deleteId);
    if (fields.id.value === deleteId) resetForm();
    render();
  }
});

cancelButton.addEventListener("click", resetForm);
loadTasks().catch((error) => setError(error.message));
