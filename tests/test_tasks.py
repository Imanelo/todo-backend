def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["docs_url"] == "/docs"


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task_minimal(client):
    payload = {"title": "Buy groceries"}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Buy groceries"
    assert data["description"] is None
    assert data["completed"] is False
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_full(client):
    payload = {
        "title": "Clean apartment",
        "description": "Living room and kitchen",
        "completed": True,
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Clean apartment"
    assert data["description"] == "Living room and kitchen"
    assert data["completed"] is True


def test_create_task_validation_error_missing_title(client):
    response = client.post("/tasks", json={"description": "Missing title"})
    assert response.status_code == 422


def test_create_task_validation_error_blank_title(client):
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 422


def test_get_task_by_id(client):
    create_res = client.post("/tasks", json={"title": "Read a book"})
    assert create_res.status_code == 201
    task_id = create_res.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Read a book"


def test_get_task_not_found(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with ID 999 not found"


def test_get_task_invalid_id_type(client):
    response = client.get("/tasks/invalid-id")
    assert response.status_code == 422


def test_list_tasks_multiple(client):
    client.post("/tasks", json={"title": "Task 1", "completed": False})
    client.post("/tasks", json={"title": "Task 2", "completed": True})
    client.post("/tasks", json={"title": "Task 3", "completed": False})

    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 3
    assert [t["title"] for t in tasks] == ["Task 1", "Task 2", "Task 3"]


def test_list_tasks_filter_by_completed(client):
    client.post("/tasks", json={"title": "Task 1", "completed": False})
    client.post("/tasks", json={"title": "Task 2", "completed": True})
    client.post("/tasks", json={"title": "Task 3", "completed": True})

    # Filter completed=true
    res_completed = client.get("/tasks?completed=true")
    assert res_completed.status_code == 200
    data_completed = res_completed.json()
    assert len(data_completed) == 2
    assert all(t["completed"] is True for t in data_completed)

    # Filter completed=false
    res_pending = client.get("/tasks?completed=false")
    assert res_pending.status_code == 200
    data_pending = res_pending.json()
    assert len(data_pending) == 1
    assert data_pending[0]["completed"] is False
    assert data_pending[0]["title"] == "Task 1"


def test_update_task_put(client):
    create_res = client.post("/tasks", json={"title": "Original Title", "description": "Original Desc"})
    task_id = create_res.json()["id"]

    update_payload = {
        "title": "Updated Title",
        "description": "Updated Desc",
        "completed": True,
    }
    response = client.put(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated Desc"
    assert data["completed"] is True


def test_update_task_patch_partial(client):
    create_res = client.post("/tasks", json={"title": "Test Patch", "description": "Keep this description"})
    task_id = create_res.json()["id"]

    # Only update completed
    response = client.patch(f"/tasks/{task_id}", json={"completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    assert data["description"] == "Keep this description"
    assert data["title"] == "Test Patch"


def test_update_task_not_found(client):
    response = client.put("/tasks/999", json={"title": "Does not exist"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with ID 999 not found"

    patch_res = client.patch("/tasks/999", json={"title": "Does not exist"})
    assert patch_res.status_code == 404
    assert patch_res.json()["detail"] == "Task with ID 999 not found"


def test_update_task_invalid_blank_title(client):
    create_res = client.post("/tasks", json={"title": "Initial"})
    task_id = create_res.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"title": "   "})
    assert response.status_code == 422


def test_delete_task_success(client):
    create_res = client.post("/tasks", json={"title": "To be deleted"})
    task_id = create_res.json()["id"]

    # Delete task
    del_res = client.delete(f"/tasks/{task_id}")
    assert del_res.status_code == 204

    # Verify it is deleted
    get_res = client.get(f"/tasks/{task_id}")
    assert get_res.status_code == 404

    # Verify task list is now empty
    list_res = client.get("/tasks")
    assert list_res.status_code == 200
    assert list_res.json() == []


def test_delete_task_not_found(client):
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with ID 999 not found"

