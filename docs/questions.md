# Django TODO Application - Homework Questions & Answers

## Question 1: Install Django

**Question:** We want to install Django. Ask AI to help you with that. What's the command you used for that?

**Answer:** 
```bash
uv add django
```

**Alternative commands:**
- `pip install django`
- `pip install django==5.2.8`
- `uv sync` (if using pyproject.toml with dependencies already defined)

**Our approach:** We used `uv` as the package manager and defined Django in `pyproject.toml`:
```toml
dependencies = [
    "django",
    "psycopg2-binary",
    "gunicorn",
]
```

---

## Question 2: Project and App

**Question:** Now we need to create a project and an app for that. Follow the instructions from AI to do it. At some point, you will need to include the app you created in the project. What's the file you need to edit for that?

**Options:**
- ✅ **settings.py** ← CORRECT ANSWER
- manage.py
- urls.py
- wsgi.py

**Answer:** `settings.py`

**Explanation:** You need to add your app to the `INSTALLED_APPS` list in `todo_project/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todos',  # ← Our app added here
]
```

**Commands used:**
```bash
# Create project
django-admin startproject todo_project .

# Create app
python manage.py startapp todos
```

---

## Question 3: Django Models

**Question:** Let's now proceed to creating models - the mapping from python objects to a relational database. For the TODO app, which models do we need? Implement them. What's the next step you need to take?

**Options:**
- Run the application
- Add the models to the admin panel
- ✅ **Run migrations** ← CORRECT ANSWER
- Create a makefile

**Answer:** Run migrations

**Explanation:** After creating models, you must create and apply migrations to update the database schema.

**Commands:**
```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

**Our Todo Model:**
```python
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

---

## Question 4: TODO Logic

**Question:** Let's now ask AI to implement the logic for the TODO app. Where do we put it?

**Options:**
- ✅ **views.py** ← CORRECT ANSWER
- urls.py
- admin.py
- tests.py

**Answer:** `views.py`

**Explanation:** Business logic and request handling goes in `views.py`. We implemented Class-Based Views (CBVs) for CRUD operations:

```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class TodoListView(ListView):
    model = Todo
    template_name = 'todos/todo_list.html'
    context_object_name = 'todos'

class TodoCreateView(CreateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todos/todo_form.html'
    success_url = reverse_lazy('todo-list')

# ... and more views
```

**Note:** 
- `urls.py` is for URL routing
- `admin.py` is for Django admin configuration
- `tests.py` is for unit tests

---

## Question 5: Templates

**Question:** Next step is creating the templates. You will need at least two: the base one and the home one. Let's call them base.html and home.html. Where do you need to register the directory with the templates?

**Options:**
- INSTALLED_APPS in project's settings.py
- ✅ **TEMPLATES['DIRS'] in project's settings.py** ← CORRECT ANSWER
- TEMPLATES['APP_DIRS'] in project's settings.py
- In the app's urls.py

**Answer:** `TEMPLATES['DIRS']` in project's `settings.py`

**Explanation:** To register project-level template directories, add them to the `DIRS` list in the `TEMPLATES` configuration:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ← Project-level templates
        'APP_DIRS': True,  # Also search in app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

**Our template structure:**
```
templates/
└── base.html                    # Project-level base template

todos/templates/todos/
├── todo_list.html              # App-specific templates
├── todo_detail.html
├── todo_form.html
└── todo_confirm_delete.html
```

---

## Question 6: Tests

**Question:** Now let's ask AI to cover our functionality with tests. Ask it which scenarios we should cover. Make sure they make sense. Let it implement it and run them. Probably it will require a few iterations to make sure that tests pass and everything is working. What's the command you use for running tests in the terminal?

**Options:**
- pytest
- ✅ **python manage.py test** ← CORRECT ANSWER
- python -m django run_tests
- django-admin test

**Answer:** `python manage.py test`

**Explanation:** Django's built-in test runner is invoked with `python manage.py test`.

**Commands:**
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test todos

# Run specific test class
python manage.py test todos.tests.TodoModelTest

# Run with verbosity
python manage.py test --verbosity=2
```

**Using our Makefile:**
```bash
make test
```

**Our test coverage:**
- ✅ **37 tests** implemented
- ✅ **~90% coverage** achieved
- ✅ **All tests passing**

**Test scenarios covered:**
1. **Model Tests** (8 tests)
   - String representation
   - Default values
   - Model ordering
   - Field validation
   - Timestamp auto-generation

2. **Form Tests** (5 tests)
   - Valid form submission
   - Required field validation
   - Optional field handling
   - Date widget rendering
   - Invalid date format handling

3. **View Tests** (21 tests)
   - List view (status code, template, content, ordering)
   - Detail view (status code, template, 404 handling)
   - Create view (GET/POST, validation, redirect)
   - Update view (GET/POST, validation, 404 handling)
   - Delete view (GET/POST, redirect)
   - Toggle resolved (POST, redirect, method restriction)

4. **Integration Tests** (3 tests)
   - Full CRUD workflow
   - Toggle resolved workflow
   - Multiple todos with different states

---

## Summary

| Question | Answer | File/Command |
|----------|--------|--------------|
| Q1: Install Django | `uv add django` | `pyproject.toml` |
| Q2: Include app in project | `settings.py` | `INSTALLED_APPS` |
| Q3: After creating models | Run migrations | `python manage.py migrate` |
| Q4: TODO logic location | `views.py` | Business logic & views |
| Q5: Register templates | `TEMPLATES['DIRS']` | `settings.py` |
| Q6: Run tests | `python manage.py test` | Django test runner |

---

## Additional Resources

- **Project Repository:** [GitHub - ai-dev-tools-zoomcamp-hw-01](https://github.com/KonuTech/ai-dev-tools-zoomcamp-hw-01)
- **Documentation:**
  - [README.md](../README.md) - Complete project documentation
  - [Testing Plan](testing_plan.md) - Comprehensive testing strategy
  - [Implementation Plan](implementation_plan.md) - Technical implementation details