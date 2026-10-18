# Task Tracker REST API

A lightweight REST API for managing tasks built with [FastAPI](https://fastapi.tiangolo.com/) and in-memory storage.

## Features

- **In-Memory Storage**: Thread-safe storage with support for task creation, retrieval, listing (with filtering), updating, and deletion.
- **Data Validation**: Strict request/response validation powered by Pydantic v2.
- **Full CRUD Endpoints**:
  - `POST /tasks`: Create a new task.
  - `GET /tasks`: List all tasks (optional `?completed=true|false` filter).
  - `GET /tasks/{id}`: Retrieve a specific task by ID.
  - `PUT /tasks/{id}`: Update an existing task.
  - `PATCH /tasks/{id}`: Partially update an existing task.
  - `DELETE /tasks/{id}`: Delete a task by ID.
- **Interactive Documentation**: Swagger UI at `/docs` and ReDoc at `/redoc`.
- **Test Suite**: Comprehensive automated tests using `pytest` and `httpx`.

---

## Getting Started

### 1. Prerequisites

- Python 3.10+

### 2. Virtual Environment Setup

The virtual environment is already initialized in `.venv`. To activate it manually:

```bash
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies if starting fresh:
pip install -r requirements.txt
```

### 3. Running the Server

Start the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Once running:
- API Root: `http://localhost:8000/`
- Interactive API Docs (Swagger): `http://localhost:8000/docs`
- Alternative Docs (ReDoc): `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`

---

## Running the Tests

Execute `pytest` using the virtual environment:

```bash
.venv/bin/pytest -v
```

All 18 unit and integration tests will run with automatic test isolation.

---

## Project Structure

```
todo-backend/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI application entrypoint
│   ├── models.py       # Pydantic schemas (TaskBase, TaskCreate, TaskUpdate, Task)
│   ├── storage.py      # Thread-safe in-memory task repository
│   └── routers/
│       ├── __init__.py
│       └── tasks.py    # CRUD task endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py     # Pytest fixtures and test client
│   └── test_tasks.py   # Comprehensive endpoint tests
├── requirements.txt    # Pinned dependencies
├── .gitignore
└── README.md
```

