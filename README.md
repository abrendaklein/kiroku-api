# Kiroku API

A REST API for managing tasks, built with Python, FastAPI and PostgreSQL. The project runs with Docker and includes automated tests.

## About the project

I'm studying back-end development and built this project to practice creating an API from scratch. It handles task records and uses PostgreSQL to store them. Along the way, I got to work with data validation, database queries, Docker and automated tests.

I mainly used the official documentation of FastAPI, SQLAlchemy and Pydantic as references. I also used AI to help me understand some concepts and debug issues along the way. I tested the code and worked through the problems as I built the project.

*Kiroku* (記録) means "record" in Japanese. I chose the name because I like Japanese culture and thought it fit a project focused on keeping track of tasks.

## Tech stack

- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- Docker and Docker Compose
- Pytest

## Project structure

```text
kiroku-api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routes.py
├── tests/
│   ├── conftest.py
│   └── test_tasks.py
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .dockerignore
└── .gitignore
```

- `main.py`: creates the app and defines the health check endpoint
- `database.py`: sets up the database connection and sessions
- `models.py`: defines the database table
- `schemas.py`: validates incoming data and defines response formats
- `routes.py`: contains the API endpoints

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/kiroku/` | Create a task |
| `GET` | `/kiroku/` | List tasks |
| `GET` | `/kiroku/{id}` | Get a task by ID |
| `PUT` | `/kiroku/{id}` | Update a task |
| `DELETE` | `/kiroku/{id}` | Delete a task |
| `GET` | `/health` | Check the API and database connection |

The task list supports pagination with the `skip` and `limit` query parameters.

Each task has a required `title` (up to 100 characters), an optional `description` (up to 500 characters) and a `completed` field that starts as `false`.

### Example

Request:

```http
POST /kiroku/
Content-Type: application/json

{
  "title": "Study Python",
  "description": "Practice APIs"
}
```

Response (`201 Created`):

```json
{
  "id": 1,
  "title": "Study Python",
  "description": "Practice APIs",
  "completed": false,
  "created_at": "2026-10-21T12:00:00Z",
  "updated_at": "2026-10-21T12:00:00Z"
}
```

### Status codes

- `200`: request successful
- `201`: task created
- `204`: task deleted
- `404`: task not found
- `422`: invalid input
- `503`: database connection failed (`/health`)

## Running the project

### With Docker

1. Create your environment file:

```powershell
   Copy-Item .env.example .env
```

   On Linux/Mac: `cp .env.example .env`

2. Fill in the values in `.env`.

3. Build and start the containers:

```bash
   docker compose up --build
```

4. Open the interactive API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

To stop the containers, press `Ctrl+C`. To remove the containers and the database volume, run:

```bash
docker compose down -v
```

**Warning:** `docker compose down -v` deletes the stored database data.

### Running the API without Docker

In this setup, PostgreSQL still runs in Docker, but the API runs directly on your machine.

1. Create and activate a virtual environment:

```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
```

   On Linux/Mac: `source .venv/bin/activate`

2. Install the dependencies:

```bash
   pip install -r requirements-dev.txt
```

3. Create `.env` from `.env.example` and set `DATABASE_URL` to use `localhost` as the host.

4. Start PostgreSQL:

```bash
   docker compose up db -d
```

5. Run the API:

```bash
   uvicorn app.main:app --reload
```

## Environment variables

The `.env` file contains local configuration and is not committed to Git. Use `.env.example` as a template.

- `POSTGRES_USER`: database username
- `POSTGRES_PASSWORD`: database password
- `POSTGRES_DB`: database name
- `DATABASE_URL`: database connection string

The connection URL depends on where the API runs. Inside Docker Compose, the database host is `db` (Compose sets this automatically). When running locally, it is `localhost`.

## Tests

Run the tests with:

```bash
pytest -v
```

The tests use an in-memory SQLite database to keep test data separate from the PostgreSQL database, so Docker doesn't need to be running. They cover task creation, listing, retrieval, updates, deletion, pagination, input validation and the health check.

## What I learned

- Building REST endpoints with FastAPI
- Working with PostgreSQL and SQLAlchemy
- Validating data and handling errors
- Using Docker and Pytest during development
