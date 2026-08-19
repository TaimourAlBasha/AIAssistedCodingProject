# Task Tracker API

A minimal FastAPI REST API skeleton for the Module 1 Task Tracker learning project.

This project uses:

- Python
- FastAPI
- Pydantic
- Uvicorn
- Local JSON file storage planned for future task CRUD endpoints

The current skeleton includes only a health check endpoint. CRUD endpoints are intentionally not included yet.

## Project Structure

```text
task-tracker-api/
├── app/
│   ├── __init__.py
│   └── main.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txtuvicorn app.main:app --reload --port 8000
