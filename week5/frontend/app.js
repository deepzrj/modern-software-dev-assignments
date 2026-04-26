async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

const pageSize = 10;
let notesPage = 1;
let actionsPage = 1;

async function loadNotes() {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  const result = await fetchJSON(`/notes/?page=${notesPage}&page_size=${pageSize}`);
  for (const n of result.items) {
    const li = document.createElement('li');
    li.textContent = `${n.title}: ${n.content}`;
    list.appendChild(li);
  }
  document.getElementById('notes-page').textContent = `Page ${result.page}`;
  document.getElementById('notes-prev').disabled = result.page <= 1;
  document.getElementById('notes-next').disabled = result.page * result.page_size >= result.total;
}

async function loadActions() {
  const list = document.getElementById('actions');
  const filter = document.getElementById('action-filter').value;
  const params = new URLSearchParams({ page: actionsPage, page_size: pageSize });
  if (filter !== '') params.set('completed', filter);

  list.innerHTML = '';
  const result = await fetchJSON(`/action-items/?${params}`);
  for (const a of result.items) {
    const li = document.createElement('li');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.value = a.id;
    checkbox.disabled = a.completed;
    checkbox.className = 'action-select';
    li.appendChild(checkbox);

    const label = document.createElement('span');
    label.textContent = ` ${a.description} [${a.completed ? 'done' : 'open'}]`;
    li.appendChild(label);

    if (!a.completed) {
      const btn = document.createElement('button');
      btn.textContent = 'Complete';
      btn.onclick = async () => {
        await fetchJSON(`/action-items/${a.id}/complete`, { method: 'PUT' });
        loadActions();
      };
      li.appendChild(btn);
    }
    list.appendChild(li);
  }
  document.getElementById('actions-page').textContent = `Page ${result.page}`;
  document.getElementById('actions-prev').disabled = result.page <= 1;
  document.getElementById('actions-next').disabled = result.page * result.page_size >= result.total;
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('note-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('note-title').value;
    const content = document.getElementById('note-content').value;
    await fetchJSON('/notes/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content }),
    });
    e.target.reset();
    notesPage = 1;
    loadNotes();
  });

  document.getElementById('action-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const description = document.getElementById('action-desc').value;
    await fetchJSON('/action-items/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description }),
    });
    e.target.reset();
    actionsPage = 1;
    loadActions();
  });

  document.getElementById('notes-prev').addEventListener('click', () => {
    notesPage -= 1;
    loadNotes();
  });
  document.getElementById('notes-next').addEventListener('click', () => {
    notesPage += 1;
    loadNotes();
  });
  document.getElementById('action-filter').addEventListener('change', () => {
    actionsPage = 1;
    loadActions();
  });
  document.getElementById('actions-prev').addEventListener('click', () => {
    actionsPage -= 1;
    loadActions();
  });
  document.getElementById('actions-next').addEventListener('click', () => {
    actionsPage += 1;
    loadActions();
  });
  document.getElementById('actions-bulk-complete').addEventListener('click', async () => {
    const ids = Array.from(document.querySelectorAll('.action-select:checked')).map((input) =>
      Number(input.value),
    );
    await fetchJSON('/action-items/bulk-complete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ids }),
    });
    loadActions();
  });

  loadNotes();
  loadActions();
});
