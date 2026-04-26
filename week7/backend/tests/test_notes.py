def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"


def test_note_validation_extract_and_delete(client):
    r = client.post("/notes/", json={"title": "  ", "content": "Body"})
    assert r.status_code == 422

    payload = {
        "title": "Planning",
        "content": "Follow-up: email the team\n2. Review PR\nFYI only",
    }
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.post(f"/notes/{note_id}/extract-action-items")
    assert r.status_code == 201
    descriptions = {item["description"] for item in r.json()}
    assert descriptions == {"Follow-up: email the team", "Review PR"}

    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404


def test_notes_pagination_sorting_and_invalid_sort(client):
    for title in ["Bravo", "Alpha", "Charlie"]:
        r = client.post("/notes/", json={"title": title, "content": f"{title} content"})
        assert r.status_code == 201

    r = client.get("/notes/", params={"sort": "title", "skip": 1, "limit": 1})
    assert r.status_code == 200
    items = r.json()
    assert [item["title"] for item in items] == ["Bravo"]

    r = client.get("/notes/", params={"sort": "-title", "limit": 2})
    assert r.status_code == 200
    assert [item["title"] for item in r.json()] == ["Charlie", "Bravo"]

    r = client.get("/notes/", params={"sort": "unknown"})
    assert r.status_code == 400
