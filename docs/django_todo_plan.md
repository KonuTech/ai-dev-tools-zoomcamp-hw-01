# Django TODO Application – Improved Technical Plan (Reordered & Docker-first)

## 0. Executive Summary (priority order)
1. **Dev environment & Docker** (make development reproducible from the start)
2. **Project scaffold** (create project/app, settings, basic urls)
3. **Core data model & migrations** (Todo model)
4. **Core CRUD endpoints & URL routing** (views, urls, forms)
5. **Templates & UX** (templates, date widgets, resolved toggles)
6. **Tests** (unit/integration tests early to guide changes)
7. **Static assets & collectstatic**
8. **Docker images, docker-compose orchestration** (dev and prod variants)
9. **CI / deployment & optional features** (auth, API, tags)

Prioritizing Docker and tests early gives consistent developer experience and reduces "works on my machine" friction.

---

## 1. Project Goal
Build a robust Django TODO application that supports create/edit/delete, due dates, resolution toggling, and easy local and containerized development. Use Python tooling and `uv` for dependency/environment management.

---

## 2. Dev Environment (Make this step first)
### Requirements
- Python ≥ 3.11
- Docker & Docker Compose (v2)
- `uv` for dependency management

### Local (non-Docker) quick setup
```sh
uv venv
source .venv/bin/activate
uv add django
```

---

## 3. Containerized Development (docker-compose) — HIGH PRIORITY
Providing a `docker-compose.yml` from start ensures every developer runs the same environment.

### Goals for compose files
- `web` service runs Django via `python manage.py runserver` (dev) or `gunicorn` (prod)
- mount code into container for live reload during development
- optional `db` service: Postgres (recommended for parity with production)
- provide `.env` to configure secrets and DB connection

### `docker-compose.yml` (development)
```yaml
version: '3.8'
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.dev
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/static
    ports:
      - "8000:8000"
    env_file:
      - .env.dev
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    ports:
      - "5432:5432"

volumes:
  postgres_data:
  static_volume:
```

### `Dockerfile.dev`
```Dockerfile
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# System deps
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Install uv (CLI) and pip-tools
RUN pip install --no-cache-dir uv

# Copy lockfiles first for caching
COPY uv.lock pyproject.toml /app/
RUN uv sync --frozen

# Copy project
COPY . /app/

# Create static dir
RUN mkdir -p /app/static

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### `.env.dev` (example)
```
DEBUG=1
SECRET_KEY=dev-secret-key
POSTGRES_DB=todo_db
POSTGRES_USER=todo_user
POSTGRES_PASSWORD=todo_pass
DB_HOST=db
DB_PORT=5432
```

### `docker-compose.prod.yml` (notes)
- Use a slim `python` base and `gunicorn` command
- Run `collectstatic` during build
- Use managed secrets and disable hot-reload volumes

---

## 4. Project Scaffold (after Docker is in place)
### Create the project & app
```sh
django-admin startproject todo_project .
python manage.py startapp todos
```

### Settings adjustments for containerized env
- Use environment variables for `DEBUG`, `SECRET_KEY`, and database configuration
- Example for `DATABASES` (Postgres if `DB_HOST` set, otherwise SQLite fallback)

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret')
DEBUG = os.getenv('DEBUG', '0') == '1'

if os.getenv('DB_HOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT', 5432),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

- Add `todos` to `INSTALLED_APPS`
- Configure `STATIC_ROOT` and `STATICFILES_DIRS`

---

## 5. Models & Migrations (core data model)
Create `Todo` model in `todos/models.py`:

```python
from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    is_resolved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["is_resolved", "due_date", "-created_at"]

    def __str__(self):
        return self.title
```

Run migrations (inside container or locally):
```sh
python manage.py makemigrations
python manage.py migrate
```

---

## 6. Core CRUD & Routing (implement quickly to get working app)
Implement views (CBVs recommended) and app URL config early so you can iterate templates against live endpoints.

### `todos/urls.py` (app-level)
```python
from django.urls import path
from .views import (
    TodoListView, TodoDetailView, TodoCreateView,
    TodoUpdateView, TodoDeleteView, toggle_resolved
)

urlpatterns = [
    path('', TodoListView.as_view(), name='todo-list'),
    path('todo/create/', TodoCreateView.as_view(), name='todo-create'),
    path('todo/<int:pk>/', TodoDetailView.as_view(), name='todo-detail'),
    path('todo/<int:pk>/edit/', TodoUpdateView.as_view(), name='todo-edit'),
    path('todo/<int:pk>/delete/', TodoDeleteView.as_view(), name='todo-delete'),
    path('todo/<int:pk>/toggle/', toggle_resolved, name='todo-toggle-resolved'),
]
```

Implement `ModelForm` for `Todo` with date widget.

---

## 7. Templates & UX
- `base.html`, `todo_list.html`, `todo_detail.html`, `todo_form.html`, `todo_confirm_delete.html`
- Use HTML5 date input for `due_date` widget
- Add CSS class `overdue` when due date passed and `is_resolved` is false
- Add pagination on list view if many items

---

## 8. Tests (write early)
- Model tests: string repr, ordering, defaults
- Form tests: validation, widget present
- View tests: list/detail/create/edit/delete/toggle using Django test client
- DB-backed integration tests (run in CI container similar to compose)

---

## 9. Static Files & Assets
- Develop with `STATICFILES_DIRS` and local `static/`
- In Docker production build, run `collectstatic --noinput` and serve static via CDN or reverse-proxy

---

## 10. Dockerfile (production) — optimized
```Dockerfile
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Install uv and runtime deps
RUN pip install --no-cache-dir uv

COPY uv.lock pyproject.toml /app/
RUN uv sync --frozen

COPY . /app/

RUN python manage.py collectstatic --noinput || true

CMD ["gunicorn", "todo_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## 11. docker-compose (production notes)
A production compose typically replaces `web` with a non-development Dockerfile, uses managed secrets, and puts a reverse proxy (nginx) in front of the app.

Example `docker-compose.prod.yml` ideas (nginx, web, db, redis for cache) — keep development `docker-compose.yml` earlier simple.

---

## 12. CI / Git Hooks / Linting
- Add `pre-commit` hooks (black, isort, flake8)
- CI pipeline (GitHub Actions) to:
  - run tests
  - build docker image
  - optionally push to registry

---

## 13. Project Folder Tree (updated)
```
project-root/
├── .venv/                 # optional local venv
├── .env.dev               # dev env vars (ignored in git)
├── .gitignore
├── Dockerfile             # production build
├── Dockerfile.dev         # development build used by compose
├── docker-compose.yml     # development compose
├── docker-compose.prod.yml# production compose (optional)
├── manage.py
├── uv.lock
├── pyproject.toml
├── todo_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── todos/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   └── test_forms.py
│   └── templates/
│       └── todos/
│           ├── todo_list.html
│           ├── todo_detail.html
│           ├── todo_form.html
│           └── todo_confirm_delete.html
├── static/
│   └── css/
│       └── styles.css
└── README.md
```

---

## 14. Future Enhancements (priority order)
1. Authentication & per-user Todos (high)
2. API endpoints (DRF) to support mobile/web clients
3. Tags/categories & filters
4. Background tasks (Celery + Redis) for reminders
5. Pagination, search, sorting UI

---

## 15. Commands (quick reference)
### Build & run locally (docker-compose dev)
```sh
docker compose up --build
# then inside web container:
# python manage.py migrate
# python manage.py createsuperuser
```

### Run tests inside container
```sh
docker compose run --rm web python manage.py test
```

### Build production image
```sh
docker build -t django-todo:latest .
```

---

If you want, I can now:
- Generate the `docker-compose.yml`, `Dockerfile.dev`, and `Dockerfile` files in the repository (ready to copy)
- Create full scaffolding (models, views, forms, templates, tests)
- Produce GitHub Actions CI config tuned to this Docker setup

Tell me which of these you'd like me to produce next and I will add it to the canvas.

