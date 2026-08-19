import pytest
from fastapi.testclient import TestClient

from app import storage
from app.main import app


@pytest.fixture
def client():
    storage._reset()
    with TestClient(app) as test_client:
        yield test_client
    storage._reset()


def test_patch_in_progress_task_back_to_todo_rejects_unsupported_transition(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Active task", "status": "InProgress"},
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"status": "ToDo"},
    )

    assert response.status_code == 422
    assert "Invalid status transition from InProgress to ToDo" in response.json()["detail"]
