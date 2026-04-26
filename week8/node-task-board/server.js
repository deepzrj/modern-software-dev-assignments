const http = require("http");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const PORT = process.env.PORT || 5009;
const DATA_FILE = path.join(__dirname, "tasks.json");
const PUBLIC_DIR = path.join(__dirname, "public");
const statuses = new Set(["todo", "doing", "done"]);
const priorities = new Set(["low", "medium", "high"]);

function readTasks() {
  if (!fs.existsSync(DATA_FILE)) return [];
  return JSON.parse(fs.readFileSync(DATA_FILE, "utf8"));
}

function writeTasks(tasks) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(tasks, null, 2));
}

function sendJson(res, status, body) {
  res.writeHead(status, { "Content-Type": "application/json" });
  res.end(JSON.stringify(body));
}

function sendFile(res, filePath) {
  const ext = path.extname(filePath);
  const types = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript" };
  fs.readFile(filePath, (error, data) => {
    if (error) {
      res.writeHead(404);
      res.end("Not found");
      return;
    }
    res.writeHead(200, { "Content-Type": types[ext] || "text/plain" });
    res.end(data);
  });
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let body = "";
    req.on("data", (chunk) => {
      body += chunk;
      if (body.length > 1_000_000) req.destroy();
    });
    req.on("end", () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (error) {
        reject(error);
      }
    });
  });
}

function validateTask(input) {
  const title = String(input.title || "").trim();
  const status = input.status || "todo";
  const priority = input.priority || "medium";
  if (!title) return { error: "Title is required." };
  if (!statuses.has(status)) return { error: "Invalid status." };
  if (!priorities.has(priority)) return { error: "Invalid priority." };
  return {
    title,
    description: String(input.description || "").trim(),
    status,
    priority
  };
}

async function handleApi(req, res) {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const parts = url.pathname.split("/").filter(Boolean);

  if (req.method === "GET" && url.pathname === "/api/tasks") {
    sendJson(res, 200, readTasks());
    return;
  }

  if (req.method === "POST" && url.pathname === "/api/tasks") {
    const input = await readBody(req);
    const data = validateTask(input);
    if (data.error) return sendJson(res, 400, data);
    const tasks = readTasks();
    const task = { id: crypto.randomUUID(), ...data, createdAt: new Date().toISOString() };
    tasks.unshift(task);
    writeTasks(tasks);
    sendJson(res, 201, task);
    return;
  }

  if (parts[0] === "api" && parts[1] === "tasks" && parts[2]) {
    const taskId = parts[2];
    const tasks = readTasks();
    const index = tasks.findIndex((task) => task.id === taskId);
    if (index === -1) return sendJson(res, 404, { error: "Task not found." });

    if (req.method === "PUT") {
      const input = await readBody(req);
      const data = validateTask(input);
      if (data.error) return sendJson(res, 400, data);
      tasks[index] = { ...tasks[index], ...data, updatedAt: new Date().toISOString() };
      writeTasks(tasks);
      sendJson(res, 200, tasks[index]);
      return;
    }

    if (req.method === "DELETE") {
      const [removed] = tasks.splice(index, 1);
      writeTasks(tasks);
      sendJson(res, 200, removed);
      return;
    }
  }

  sendJson(res, 404, { error: "Not found." });
}

const server = http.createServer((req, res) => {
  if (req.url.startsWith("/api/")) {
    handleApi(req, res).catch(() => sendJson(res, 400, { error: "Invalid request." }));
    return;
  }

  const urlPath = req.url === "/" ? "/index.html" : req.url;
  const filePath = path.join(PUBLIC_DIR, path.normalize(urlPath));
  if (!filePath.startsWith(PUBLIC_DIR)) {
    res.writeHead(403);
    res.end("Forbidden");
    return;
  }
  sendFile(res, filePath);
});

server.listen(PORT, () => {
  console.log(`Node Task Board running at http://127.0.0.1:${PORT}`);
});
