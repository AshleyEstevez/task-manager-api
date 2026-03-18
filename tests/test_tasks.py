import pytest

@pytest.fixture
def auth_header(client):
    client.post(
        "/register",
        json={"email": "test@example.com", "password": "password123"},
    )
    response = client.post(
        "/token",
        data={"username": "test@example.com", "password": "password123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_task(client, auth_header):
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Test Description"},
        headers=auth_header,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert "id" in data

def test_read_tasks(client, auth_header):
    client.post(
        "/tasks/",
        json={"title": "Task 1", "description": "Description 1"},
        headers=auth_header,
    )
    client.post(
        "/tasks/",
        json={"title": "Task 2", "description": "Description 2"},
        headers=auth_header,
    )
    response = client.get("/tasks/", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"

def test_read_task(client, auth_header):
    create_response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Test Description"},
        headers=auth_header,
    )
    task_id = create_response.json()["id"]
    response = client.get(f"/tasks/{task_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_read_non_existent_task(client, auth_header):
    response = client.get("/tasks/999", headers=auth_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_update_task(client, auth_header):
    create_response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Test Description"},
        headers=auth_header,
    )
    task_id = create_response.json()["id"]
    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated Task", "completed": True},
        headers=auth_header,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["completed"] is True

def test_delete_task(client, auth_header):
    create_response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Test Description"},
        headers=auth_header,
    )
    task_id = create_response.json()["id"]
    response = client.delete(f"/tasks/{task_id}", headers=auth_header)
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/tasks/{task_id}", headers=auth_header)
    assert get_response.status_code == 404

def test_access_another_user_task(client):
    # Create user 1 and a task
    client.post("/register", json={"email": "u1@ex.com", "password": "p1"})
    r1 = client.post("/token", data={"username": "u1@ex.com", "password": "p1"})
    t1 = r1.json()["access_token"]
    h1 = {"Authorization": f"Bearer {t1}"}
    
    cr1 = client.post("/tasks/", json={"title": "U1 Task"}, headers=h1)
    task_id = cr1.json()["id"]
    
    # Create user 2
    client.post("/register", json={"email": "u2@ex.com", "password": "p2"})
    r2 = client.post("/token", data={"username": "u2@ex.com", "password": "p2"})
    t2 = r2.json()["access_token"]
    h2 = {"Authorization": f"Bearer {t2}"}
    
    # Try to access U1's task with U2's token
    response = client.get(f"/tasks/{task_id}", headers=h2)
    assert response.status_code == 404
