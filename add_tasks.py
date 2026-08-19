import requests

tasks = [
    {"title": "Write project requirements", "description": "Capture scope, acceptance criteria, and API surface for the task tracker.", "priority": "High", "assignee": None, "status": "ToDo"},
    {"title": "Estimate work effort", "description": "Provide time estimates for each major task.", "priority": "Medium", "assignee": "Lina", "status": "ToDo"},
    {"title": "Design the board layout", "description": "Create the page structure and sample task card design.", "priority": "Medium", "assignee": "Jamie", "status": "InProgress"},
    {"title": "Implement API validation", "description": "Add validation rules to ensure correct task payloads.", "priority": "High", "assignee": "Priya", "status": "InProgress"},
    {"title": "Set up repository", "description": "Initialize the repo and verify directories are in place.", "priority": "Low", "assignee": "Alex", "status": "Done"},
    {"title": "Confirm design tokens", "description": "Review color and spacing tokens used in the UI.", "priority": "Low", "assignee": None, "status": "Done"},
]

for task in tasks:
    response = requests.post("http://localhost:8000/tasks", json=task)
    if response.status_code == 201:
        print(f"Added: {task['title']}")
    else:
        print(f"Failed to add {task['title']}: {response.status_code}")

print("Done!")
