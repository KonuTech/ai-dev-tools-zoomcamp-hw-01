# Django TODO Application Implementation Plan

Based on the user-provided plan, we will build a Docker-first Django application.

## User Review Required
- **Dependency Management**: We will use `uv` as requested.
- **Database**: Postgres for Docker environment, SQLite fallback for local non-Docker dev (if needed), but primarily focusing on Docker-compose workflow.

## Proposed Changes

### Infrastructure & Configuration
#### [NEW] [Dockerfile.dev](file:///c:/Users/borow/VSC/projects/ai-dev-tools-zoomcamp-hw-01/Dockerfile.dev)
- Development Dockerfile using python:3.12-slim.
- Installs `uv`.

#### [NEW] [docker-compose.yml](file:///c:/Users/borow/VSC/projects/ai-dev-tools-zoomcamp-hw-01/docker-compose.yml)
- Services: `web` (Django), `db` (Postgres).
- Volumes for code reloading.

#### [NEW] [pyproject.toml](file:///c:/Users/borow/VSC/projects/ai-dev-tools-zoomcamp-hw-01/pyproject.toml)
- Python project configuration.

### Django Project Structure
#### [NEW] [manage.py](file:///c:/Users/borow/VSC/projects/ai-dev-tools-zoomcamp-hw-01/manage.py)
- Standard Django entry point.

#### [NEW] [todo_project/](file:///c:/Users/borow/VSC/projects/ai-dev-tools-zoomcamp-hw-01/todo_project/)
- Project settings and configuration.
- `settings.py`: Adjusted for Docker env vars.

#### [NEW] [todos/](file:///c:/Users/borow/VSC/projects/ai-dev-tools-zoomcamp-hw-01/todos/)
- The main app.
- `models.py`: `Todo` model.
- `views.py`: CRUD views.
- `urls.py`: App-specific URLs.
- `templates/todos/`: HTML templates.

## Verification Plan

### Automated Tests
- Run `python manage.py test` inside the container.
- Test models, views, and forms.

### Manual Verification
- Spin up `docker compose up`.
- Access `http://localhost:8000`.
- Verify Create, Read, Update, Delete flows for Todos.
- Verify "Resolved" toggle.
