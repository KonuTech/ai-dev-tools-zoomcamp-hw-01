# Django TODO Application

A modern, Docker-first TODO list web application built with Django, PostgreSQL, and Bootstrap 5.

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![Django](https://img.shields.io/badge/django-5.2+-green.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Development](#development)
- [Testing](#testing)
- [Documentation](#documentation)
- [Contributing](#contributing)

## ✨ Features

- ✅ **Full CRUD Operations** - Create, Read, Update, Delete todos
- 🔄 **Status Toggle** - Mark todos as resolved/unresolved
- 📅 **Due Dates** - Set and track due dates with HTML5 date picker
- 🎨 **Modern UI** - Bootstrap 5 responsive design
- 🐳 **Docker-First** - Fully containerized development environment
- 🗄️ **PostgreSQL** - Production-ready database
- 🧪 **Tested** - Unit and integration tests included
- ⚡ **Fast Setup** - One-command deployment with Makefile

## 🛠️ Tech Stack

### Backend
- **Django 5.2+** - Python web framework
- **PostgreSQL 15** - Relational database
- **Gunicorn** - WSGI HTTP server

### Frontend
- **Bootstrap 5** - CSS framework
- **HTML5** - Semantic markup
- **Vanilla CSS** - Custom styling

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **uv** - Fast Python package manager
- **Make** - Task automation

## 📁 Project Structure

\`\`\`
ai-dev-tools-zoomcamp-hw-01/
├── todo_project/          # Django project configuration
│   ├── settings.py        # Project settings (DB, apps, middleware)
│   ├── urls.py            # Root URL configuration
│   ├── wsgi.py            # WSGI entry point
│   └── asgi.py            # ASGI entry point
├── todos/                 # Main TODO app
│   ├── models.py          # Todo model definition
│   ├── views.py           # CRUD views (CBVs)
│   ├── urls.py            # App URL patterns
│   ├── forms.py           # TodoForm with date widget
│   ├── tests.py           # Unit & integration tests
│   ├── templates/         # HTML templates
│   │   └── todos/
│   │       ├── todo_list.html
│   │       ├── todo_detail.html
│   │       ├── todo_form.html
│   │       └── todo_confirm_delete.html
│   └── migrations/        # Database migrations
├── templates/             # Project-level templates
│   └── base.html          # Base template with Bootstrap
├── static/                # Static files
│   └── css/
│       └── styles.css     # Custom CSS
├── docs/                  # Documentation
│   ├── django_todo_plan.md
│   ├── implementation_plan.md
│   └── testing_plan.md
├── Dockerfile.dev         # Development Docker image
├── docker-compose.yml     # Docker Compose configuration
├── Makefile               # Task automation
├── pyproject.toml         # Python dependencies (uv)
├── uv.lock                # Locked dependencies
└── .env                   # Environment variables (not in git)
\`\`\`

## 🚀 Quick Start

### Prerequisites

- **Docker** & **Docker Compose** (v2+)
- **Make** (optional, for convenience commands)

### Installation

1. **Clone the repository**
   \`\`\`bash
   git clone https://github.com/KonuTech/ai-dev-tools-zoomcamp-hw-01.git
   cd ai-dev-tools-zoomcamp-hw-01
   \`\`\`

2. **Create environment file**
   \`\`\`bash
   cp .env.example .env
   # Edit .env if needed (defaults work for development)
   \`\`\`

3. **Build and start the application**
   \`\`\`bash
   make build
   \`\`\`

4. **Run migrations**
   \`\`\`bash
   make migrate
   \`\`\`

5. **Access the application**
   
   Open your browser and navigate to: **http://localhost:8000**

## 📖 Usage

### Makefile Commands

The project includes a Makefile for easy management:

\`\`\`bash
make help              # Show all available commands
make up                # Start the application
make down              # Stop the application
make build             # Build and start (use after code changes)
make restart           # Restart containers
make logs              # View application logs
make migrate           # Run database migrations
make test              # Run test suite
make shell             # Open Django shell
make createsuperuser   # Create admin user
make clean             # Remove all containers and volumes
\`\`\`

### Manual Docker Commands

If you prefer not to use Make:

\`\`\`bash
# Start
docker compose up -d

# Stop
docker compose down

# View logs
docker compose logs -f

# Run migrations
docker compose run --rm web python manage.py migrate

# Run tests
docker compose run --rm web python manage.py test
\`\`\`

### Creating Your First TODO

1. Navigate to http://localhost:8000
2. Click **"Add Todo"**
3. Fill in:
   - **Title** (required)
   - **Description** (optional)
   - **Due Date** (optional)
4. Click **"Save"**

### Managing TODOs

- **View Details**: Click on a todo title
- **Edit**: Click the "Edit" button
- **Delete**: Click the "Delete" button and confirm
- **Toggle Status**: Click "Resolve" or "Reopen"

## 🔧 Development

### Local Development (without Docker)

1. **Install uv** (if not already installed)
   \`\`\`bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   \`\`\`

2. **Create virtual environment and install dependencies**
   \`\`\`bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv sync
   \`\`\`

3. **Run migrations**
   \`\`\`bash
   python manage.py migrate
   \`\`\`

4. **Start development server**
   \`\`\`bash
   python manage.py runserver
   \`\`\`

### Environment Variables

Create a \`.env\` file in the project root:

\`\`\`env
DEBUG=1
SECRET_KEY=your-secret-key-here
POSTGRES_DB=todo_db
POSTGRES_USER=todo_user
POSTGRES_PASSWORD=todo_pass
DB_HOST=db
DB_PORT=5432
\`\`\`

### Database Configuration

The app uses **PostgreSQL** in Docker and **SQLite** as a fallback for local development.

- **Docker**: Postgres 15 (configured in \`docker-compose.yml\`)
- **Local**: SQLite (if \`DB_HOST\` is not set)

## 🧪 Testing

### Running Tests

\`\`\`bash
# Using Make
make test

# Using Docker Compose
docker compose run --rm web python manage.py test

# Run specific test
docker compose run --rm web python manage.py test todos.tests.TodoModelTest
\`\`\`

### Test Coverage

Current test coverage: **~60%** (7 tests passing)

Tests include:
- ✅ Model tests (string representation, defaults)
- ✅ View tests (CRUD operations, status codes)
- ✅ Integration tests (database operations)

See [docs/testing_plan.md](docs/testing_plan.md) for the comprehensive testing strategy.

### Writing Tests

Tests are located in \`todos/tests.py\`. Example:

\`\`\`python
from django.test import TestCase
from todos.models import Todo

class TodoModelTest(TestCase):
    def test_string_representation(self):
        todo = Todo(title="Test Todo")
        self.assertEqual(str(todo), "Test Todo")
\`\`\`

## 📚 Documentation

- **[Implementation Plan](docs/implementation_plan.md)** - Technical implementation details
- **[Testing Plan](docs/testing_plan.md)** - Comprehensive testing strategy
- **[Original Plan](docs/django_todo_plan.md)** - Initial project planning

## 🏗️ Architecture

### Django Project Structure

- **\`todo_project/\`** - Project-level configuration (settings, root URLs)
- **\`todos/\`** - Self-contained app for TODO functionality

This follows Django's recommended **project → apps** architecture, allowing for:
- Modularity (easy to add more apps)
- Reusability (apps can be extracted)
- Clear separation of concerns

### Data Model

\`\`\`python
class Todo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
\`\`\`

### Views

The app uses Django's **Class-Based Views (CBVs)**:
- \`TodoListView\` - Display all todos
- \`TodoDetailView\` - Show single todo
- \`TodoCreateView\` - Create new todo
- \`TodoUpdateView\` - Edit existing todo
- \`TodoDeleteView\` - Delete todo
- \`toggle_resolved\` - Toggle todo status (function-based)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (\`git checkout -b feature/amazing-feature\`)
3. Commit your changes (\`git commit -m 'Add amazing feature'\`)
4. Push to the branch (\`git push origin feature/amazing-feature\`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed
- Keep commits atomic and descriptive

## 🐛 Troubleshooting

### Port Already Allocated

If you see "port is already allocated" error:

\`\`\`bash
# Stop all containers
docker compose down

# Remove conflicting containers
docker container prune -f

# Try again
make up
\`\`\`

### Database Connection Issues

\`\`\`bash
# Check if database container is running
docker compose ps

# View database logs
docker compose logs db

# Restart database
docker compose restart db
\`\`\`

### Migration Issues

\`\`\`bash
# Reset migrations (WARNING: deletes data)
docker compose down -v
docker compose up -d
make migrate
\`\`\`

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Konrad Borowiecki**
- GitHub: [@KonuTech](https://github.com/KonuTech)

## 🙏 Acknowledgments

- Built as part of the AI Dev Tools Zoomcamp
- Inspired by modern Django best practices
- Docker-first approach for consistent development environments

---

**Happy TODO-ing! 📝✨**