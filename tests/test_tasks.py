import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient

from app import storage
from app.main import app


@pytest.fixture
def client():
    storage._reset()
    with TestClient(app) as test_client:
        yield test_client
    storage._reset()


def test_get_version_returns_application_version(client):
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {"version": "0.1.0"}


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


def test_create_task_with_valid_due_date(client):
    response = client.post(
        "/tasks",
        json={"title": "Dated task", "due_date": "2026-09-15"},
    )

    assert response.status_code == 201
    assert response.json()["due_date"] == "2026-09-15"


def test_create_task_rejects_invalid_due_date(client):
    response = client.post(
        "/tasks",
        json={"title": "Invalid date", "due_date": "2026-02-30"},
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][-1] == "due_date"


def test_overdue_filter_includes_incomplete_and_excludes_completed_tasks(client):
    overdue_date = (date.today() - timedelta(days=1)).isoformat()
    incomplete = client.post(
        "/tasks",
        json={"title": "Late work", "due_date": overdue_date},
    ).json()
    client.post(
        "/tasks",
        json={"title": "Finished work", "due_date": overdue_date, "status": "Done"},
    )

    response = client.get("/tasks", params={"overdue": "true"})

    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [incomplete["id"]]


def test_update_preserves_and_clears_due_date(client):
    created = client.post(
        "/tasks",
        json={"title": "Scheduled work", "due_date": "2026-09-15"},
    ).json()

    preserved = client.patch(
        f"/tasks/{created['id']}",
        json={"assignee": "Lina"},
    )
    cleared = client.patch(
        f"/tasks/{created['id']}",
        json={"due_date": None},
    )

    assert preserved.status_code == 200
    assert preserved.json()["due_date"] == "2026-09-15"
    assert cleared.status_code == 200
    assert cleared.json()["due_date"] is None


def test_create_task_normalizes_and_deduplicates_tags(client):
    response = client.post(
        "/tasks",
        json={"title": "Tagged task", "tags": [" API ", "api", "Frontend"]},
    )

    assert response.status_code == 201
    assert response.json()["tags"] == ["API", "Frontend"]


def test_create_task_rejects_blank_tag(client):
    response = client.post(
        "/tasks",
        json={"title": "Invalid tags", "tags": ["backend", "   "]},
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][-1] == "tags"


def test_update_tags_and_preserve_them_during_unrelated_update(client):
    created = client.post(
        "/tasks",
        json={"title": "Tagged task", "tags": ["backend"]},
    ).json()

    updated = client.patch(
        f"/tasks/{created['id']}",
        json={"tags": ["API", "Docs"]},
    )
    preserved = client.patch(
        f"/tasks/{created['id']}",
        json={"priority": "High"},
    )

    assert updated.status_code == 200
    assert updated.json()["tags"] == ["API", "Docs"]
    assert preserved.status_code == 200
    assert preserved.json()["tags"] == ["API", "Docs"]


def test_filter_tasks_by_tag_case_insensitively(client):
    matching = client.post(
        "/tasks",
        json={"title": "API task", "tags": ["Backend"]},
    ).json()
    client.post(
        "/tasks",
        json={"title": "Design task", "tags": ["Design"]},
    )

    response = client.get("/tasks", params={"tag": "backend"})

    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [matching["id"]]


def test_combines_overdue_and_tag_filters(client):
    overdue_date = (date.today() - timedelta(days=1)).isoformat()
    matching = client.post(
        "/tasks",
        json={"title": "Late API task", "due_date": overdue_date, "tags": ["API"]},
    ).json()
    client.post(
        "/tasks",
        json={"title": "Late design task", "due_date": overdue_date, "tags": ["Design"]},
    )
    client.post(
        "/tasks",
        json={"title": "Future API task", "due_date": "2999-01-01", "tags": ["API"]},
    )

    response = client.get(
        "/tasks",
        params={"overdue": "true", "tag": "api"},
    )

    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [matching["id"]]
