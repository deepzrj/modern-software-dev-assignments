def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_list_action_items_paginates(client):
    for i in range(3):
        r = client.post("/action-items/", json={"description": f"Task {i}"})
        assert r.status_code == 201

    r = client.get("/action-items/", params={"page": 2, "page_size": 2})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 3
    assert data["page"] == 2
    assert data["page_size"] == 2
    assert len(data["items"]) == 1


def test_filter_action_items_by_completed(client):
    open_item = client.post("/action-items/", json={"description": "Open"}).json()
    done_item = client.post("/action-items/", json={"description": "Done"}).json()
    r = client.put(f"/action-items/{done_item['id']}/complete")
    assert r.status_code == 200

    r = client.get("/action-items/", params={"completed": False})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert data["items"][0]["id"] == open_item["id"]

    r = client.get("/action-items/", params={"completed": True})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert data["items"][0]["id"] == done_item["id"]


def test_bulk_complete_action_items(client):
    first = client.post("/action-items/", json={"description": "First"}).json()
    second = client.post("/action-items/", json={"description": "Second"}).json()

    r = client.post("/action-items/bulk-complete", json={"ids": [first["id"], second["id"]]})
    assert r.status_code == 200
    items = r.json()
    assert {item["id"] for item in items} == {first["id"], second["id"]}
    assert all(item["completed"] is True for item in items)


def test_bulk_complete_rolls_back_when_item_missing(client):
    item = client.post("/action-items/", json={"description": "Still open"}).json()

    r = client.post("/action-items/bulk-complete", json={"ids": [item["id"], 999]})
    assert r.status_code == 404

    r = client.get("/action-items/", params={"completed": False})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert data["items"][0]["id"] == item["id"]
