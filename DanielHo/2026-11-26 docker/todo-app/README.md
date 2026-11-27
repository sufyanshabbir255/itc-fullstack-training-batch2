# To-Do Application API

A simple Task Management REST API built with FastAPI and Docker.

## Features

- Create tasks
- View all tasks
- View a single task
- Update tasks
- Partially update tasks
- Delete tasks
- In-memory storage
- Interactive Swagger documentation

---

## Project Structure

```text
app/
├── db/
│   └── local_db.py
├── routers/
│   └── tasks.py
├── schemas/
│   └── task.py
├── main.py
│
Dockerfile
docker-compose.yml
requirements.txt
README.md
```

---

## Prerequisites

Install:

- Docker
- Docker Compose

Verify installation:

```bash
docker --version
docker compose version
```

---

## Build the Docker Image

From the project root:

```bash
docker build -t todo-api .
```

Verify:

```bash
docker images
```

---

## Run the Container

```bash
docker run -p 8000:8000 todo-api
```

The API will be available at:

```text
http://localhost:8000
```

---

## Run with Docker Compose

Start the application:

```bash
docker compose up --build
```

Run in detached mode:

```bash
docker compose up -d --build
```

Stop the application:

```bash
docker compose down
```

---

## API Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

## Available Endpoints

### Get all tasks

```http
GET /tasks
```

### Get task by ID

```http
GET /tasks/{task_id}
```

### Create task

```http
POST /tasks
```

Example request body:

```json
{
  "text": "Clean the dishes",
  "priority": "High"
}
```

### Replace task

```http
PUT /tasks/{task_id}
```

### Update task partially

```http
PATCH /tasks/{task_id}
```

Example request body:

```json
{
  "isComplete": true
}
```

### Delete task

```http
DELETE /tasks/{task_id}
```

---

## Root Endpoint

```http
GET /
```

Response:

```json
{
  "message": "Welcome to the To-Do Application"
}
```

---

## Development

Run locally without Docker:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000/docs
```

---

## Notes

- Data is stored in memory.
- All data is reset when the application restarts.
- Initial sample tasks are loaded automatically during application startup using FastAPI lifespan events.
