def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] >= 1
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert len(data["items"]) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_list_notes_paginates(client):
    for i in range(3):
        r = client.post("/notes/", json={"title": f"Note {i}", "content": "Body"})
        assert r.status_code == 201

    r = client.get("/notes/", params={"page": 2, "page_size": 2})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 3
    assert data["page"] == 2
    assert data["page_size"] == 2
    assert len(data["items"]) == 1


def test_list_notes_empty_page(client):
    r = client.post("/notes/", json={"title": "Only", "content": "Body"})
    assert r.status_code == 201

    r = client.get("/notes/", params={"page": 99, "page_size": 10})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert data["items"] == []
