# Task & Comment CRUD API

A full-stack application for managing tasks and comments, featuring a robust backend API built with Python (Flask, SQLAlchemy) and a modern frontend using React and TypeScript. The project is designed for simple yet scalable task management with comment support, suitable for teams or personal productivity.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Folder Structure](#folder-structure)
- [Scripts](#scripts)
- [Development](#development)
- [License](#license)

---

## Features

- **Task Management**: Create, read, update, and delete tasks.
- **Comment System**: Add, edit, or remove comments tied to tasks.
- **RESTful API**: Backend exposes endpoints for all CRUD operations.
- **Frontend Dashboard**: React-based dashboard UI to manage tasks and comments.
- **Database Migrations**: Alembic for schema changes and sample data seeding.
- **Automated Setup**: One-click scripts for installing dependencies, initializing the database, and starting servers.
- **Docker Support**: Containerized backend for easy deployment.
- **API Documentation**: Interactive docs (Swagger/OpenAPI) on `/api`.

---

## Architecture

- **Backend**: Python Flask application structured with blueprints, models, services, and schemas. Uses SQLAlchemy ORM and Alembic migrations.
- **Frontend**: React (TypeScript) SPA with components for tasks, comments, forms, and hooks for API calls.
- **Database**: Relational schema with `tasks` and `comments` tables. Comments are linked to tasks via foreign keys (`on delete cascade`).
- **DevOps**: Dockerfile for backend containerization, PowerShell and Batch scripts for quick setup and server management.

---

## Tech Stack

| Layer      | Technology                |
|------------|--------------------------|
| Backend    | Python, Flask, SQLAlchemy, Alembic, Flask-Migrate, Flask-CORS |
| Frontend   | React, TypeScript, Axios, CSS |
| Database   | SQLite (dev), PostgreSQL (prod-ready) |
| DevOps     | Docker, PowerShell, Batchfile |

---

## Setup & Installation

### Automated Setup (Recommended)

#### Windows

Double-click `SETUP.bat` or run in terminal:
```sh
SETUP.bat
```
#### PowerShell (Cross-platform)

```sh
./setup.ps1
```
Options:
- Installs all dependencies for frontend and backend
- Initializes and seeds the database
- Configures VS Code settings
- Optionally starts development servers

#### Manual Setup

1. **Clone the repo**
    ```sh
    git clone https://github.com/yaser0004/crud-comment-api.git
    cd crud-comment-api
    ```

2. **Backend**
    ```sh
    cd backend
    python -m venv venv
    source venv/bin/activate   # or venv\Scripts\activate (Windows)
    pip install -r requirements.txt
    flask db upgrade
    flask seed_db
    python run.py
    ```

3. **Frontend**
    ```sh
    cd frontend
    npm install
    npm start
    ```

#### Docker

```sh
docker-compose up --build
```

---

## Usage

- **Frontend**: Open [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:5000](http://localhost:5000)
- **API Documentation**: [http://localhost:5000/api](http://localhost:5000/api)

---

## API Documentation

Interactive Swagger UI available at `/api` endpoint. You can explore all endpoints, request/response formats, and model schemas.

### Main Endpoints

- **Tasks**
    - `GET /api/tasks` — List tasks
    - `POST /api/tasks` — Create new task
    - `PUT /api/tasks/{id}` — Update task
    - `DELETE /api/tasks/{id}` — Remove task

- **Comments**
    - `GET /api/tasks/{task_id}/comments` — List comments for a task
    - `POST /api/tasks/{task_id}/comments` — Add comment to a task
    - `PUT /api/comments/{id}` — Update comment
    - `DELETE /api/comments/{id}` — Remove comment

---

## Folder Structure

```
crud-comment-api/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── services/
│   │   ├── schemas/
│   │   ├── routes/
│   │   └── __init__.py
│   ├── migrations/
│   ├── requirements.txt
│   ├── run.py
│   └── Dockerfile
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── styles/
│   │   └── types/
│   └── package.json
├── setup.ps1
├── start.ps1
├── SETUP.bat
└── LICENSE
```

---

## Scripts

- **setup.ps1 / SETUP.bat**: Full install, database migration, seed data, and server start.
- **start.ps1**: Starts backend and frontend servers.
- **Dockerfile**: Build backend container.

---

## Development

- **Backend**: Flask app, entry in `backend/run.py`, supports CLI commands (`init_db`, `seed_db`) for database management.
- **Frontend**: React SPA, main page is Dashboard (`frontend/src/pages/Dashboard.tsx`), uses hooks and components for task & comment logic.
- **Database**: Alembic migration scripts in `backend/migrations/` track schema changes.

### Sample Data

After setup, the database will be seeded with example tasks:
- "Implement user authentication"
- "Create dashboard UI"
- "Write API documentation"

And sample comments linking to those tasks.

### Configuration

- Development, Testing, and Production configs supported (see `backend/app/__init__.py`).
- CORS enabled for frontend-backend communication.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Contributing

Feel free to fork and submit pull requests. Issues and suggestions are welcome!

---

## Maintainer

- [yaser0004](https://github.com/yaser0004)

---
