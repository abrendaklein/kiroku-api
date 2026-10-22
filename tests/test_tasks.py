def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "connected"}


def test_create_kiroku(client):
    response = client.post(
        "/kiroku/",
        json={"title": "Study Python", "description": "Practice API"}
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Study Python"
    assert response.json()["completed"] is False


def test_list_kiroku(client):
    client.post("/kiroku/", json={"title": "Read a book"})

    response = client.get("/kiroku/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_missing_kiroku(client):
    response = client.get("/kiroku/999")

    assert response.status_code == 404


def test_delete_kiroku(client):
    created = client.post("/kiroku/", json={"title": "Delete me"})
    kiroku_id = created.json()["id"]

    response = client.delete(f"/kiroku/{kiroku_id}")

    assert response.status_code == 204
    assert client.get(f"/kiroku/{kiroku_id}").status_code == 404


def test_update_kiroku(client):
    created = client.post("/kiroku/", json={"title": "Study Python"})
    kiroku_id = created.json()["id"]

    response = client.put(
        f"/kiroku/{kiroku_id}",
        json={"completed": True}
    )

    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_create_kiroku_without_title(client):
    response = client.post(
        "/kiroku/",
        json={"description": "No title"}
    )

    assert response.status_code == 422
    
def test_update_title_with_null(client):
    created = client.post("/kiroku/", json={"title": "Study Python"})
    kiroku_id = created.json()["id"]

    response = client.put(
        f"/kiroku/{kiroku_id}",
        json={"title": None}
    )

    assert response.status_code == 422


def test_update_completed_with_null(client):
    created = client.post("/kiroku/", json={"title": "Study Python"})
    kiroku_id = created.json()["id"]

    response = client.put(
        f"/kiroku/{kiroku_id}",
        json={"completed": None}
    )

    assert response.status_code == 422


def test_get_existing_kiroku(client):
    created = client.post("/kiroku/", json={"title": "Study Python"})
    kiroku_id = created.json()["id"]

    response = client.get(f"/kiroku/{kiroku_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Study Python"


def test_update_missing_kiroku(client):
    response = client.put("/kiroku/999", json={"completed": True})

    assert response.status_code == 404


def test_delete_missing_kiroku(client):
    response = client.delete("/kiroku/999")

    assert response.status_code == 404


def test_create_empty_title(client):
    response = client.post("/kiroku/", json={"title": ""})

    assert response.status_code == 422


def test_create_long_title(client):
    response = client.post("/kiroku/", json={"title": "a" * 101})

    assert response.status_code == 422


def test_update_completed_keeps_title(client):
    created = client.post("/kiroku/", json={"title": "Study Python"})
    kiroku_id = created.json()["id"]

    response = client.put(
        f"/kiroku/{kiroku_id}",
        json={"completed": True}
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Study Python"
    assert response.json()["completed"] is True


# extra="forbid" in the schema should reject unknown fields
def test_update_unknown_field(client):
    created = client.post("/kiroku/", json={"title": "Study Python"})
    kiroku_id = created.json()["id"]

    response = client.put(f"/kiroku/{kiroku_id}", json={"foo": "bar"})

    assert response.status_code == 422


# description is nullable in the db, so null is allowed here
def test_update_description_with_null(client):
    created = client.post(
        "/kiroku/",
        json={"title": "Study Python", "description": "something"}
    )
    kiroku_id = created.json()["id"]

    response = client.put(f"/kiroku/{kiroku_id}", json={"description": None})

    assert response.status_code == 200
    assert response.json()["description"] is None


def test_list_pagination(client):
    for i in range(3):
        client.post("/kiroku/", json={"title": f"Task {i}"})

    response = client.get("/kiroku/?skip=1&limit=1")

    assert response.status_code == 200
    assert len(response.json()) == 1