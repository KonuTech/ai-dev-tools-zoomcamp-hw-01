from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
from todos.models import Todo
from todos.forms import TodoForm


class TodoModelTest(TestCase):
    """Unit tests for the Todo model"""
    
    def test_string_representation(self):
        """Test the __str__ method returns the title"""
        todo = Todo(title="Test Todo")
        self.assertEqual(str(todo), "Test Todo")

    def test_default_values(self):
        """Test default values for new todos"""
        todo = Todo.objects.create(title="Test Todo")
        self.assertFalse(todo.is_resolved)
        self.assertIsNone(todo.due_date)
        self.assertIsNotNone(todo.created_at)
        self.assertIsNotNone(todo.updated_at)
    
    def test_model_ordering(self):
        """Test that todos are ordered by is_resolved, due_date, -created_at"""
        # Create todos with different states
        todo1 = Todo.objects.create(
            title="Resolved Old",
            is_resolved=True,
            due_date=date.today() - timedelta(days=5)
        )
        todo2 = Todo.objects.create(
            title="Unresolved Soon",
            is_resolved=False,
            due_date=date.today() + timedelta(days=1)
        )
        todo3 = Todo.objects.create(
            title="Unresolved Later",
            is_resolved=False,
            due_date=date.today() + timedelta(days=5)
        )
        
        # Get all todos in default order
        todos = list(Todo.objects.all())
        
        # Unresolved should come before resolved
        self.assertEqual(todos[0].title, "Unresolved Soon")
        self.assertEqual(todos[1].title, "Unresolved Later")
        self.assertEqual(todos[2].title, "Resolved Old")
    
    def test_field_validation_max_length(self):
        """Test title max_length validation"""
        long_title = "x" * 256  # Exceeds max_length of 255
        todo = Todo(title=long_title)
        with self.assertRaises(Exception):
            todo.full_clean()
    
    def test_description_can_be_blank(self):
        """Test that description field can be blank"""
        todo = Todo.objects.create(title="Test", description="")
        self.assertEqual(todo.description, "")
    
    def test_due_date_can_be_null(self):
        """Test that due_date can be null"""
        todo = Todo.objects.create(title="Test", due_date=None)
        self.assertIsNone(todo.due_date)
    
    def test_timestamp_auto_generation(self):
        """Test that created_at and updated_at are auto-generated"""
        todo = Todo.objects.create(title="Test")
        self.assertIsNotNone(todo.created_at)
        self.assertIsNotNone(todo.updated_at)
        
        # Test that updated_at changes on save
        original_updated = todo.updated_at
        todo.title = "Updated"
        todo.save()
        self.assertGreater(todo.updated_at, original_updated)


class TodoFormTest(TestCase):
    """Unit tests for the TodoForm"""
    
    def test_valid_form_submission(self):
        """Test form with valid data"""
        form_data = {
            'title': 'Test Todo',
            'description': 'Test Description',
            'due_date': date.today(),
            'is_resolved': False
        }
        form = TodoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_required_field_validation(self):
        """Test that title is required"""
        form_data = {
            'description': 'Test Description',
        }
        form = TodoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_optional_field_handling(self):
        """Test that description and due_date are optional"""
        form_data = {
            'title': 'Test Todo',
        }
        form = TodoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_date_widget_rendering(self):
        """Test that date widget is rendered correctly"""
        form = TodoForm()
        self.assertIn('type="date"', str(form['due_date']))
    
    def test_invalid_date_format(self):
        """Test handling of invalid date format"""
        form_data = {
            'title': 'Test Todo',
            'due_date': 'invalid-date',
        }
        form = TodoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)


class TodoListViewTest(TestCase):
    """Tests for the Todo list view"""
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('todo-list')
    
    def test_list_view_status_code(self):
        """Test that list view returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_list_view_template(self):
        """Test correct template is used"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todos/todo_list.html')
    
    def test_list_view_contains_todos(self):
        """Test that todos appear in the list"""
        Todo.objects.create(title="Test Todo 1")
        Todo.objects.create(title="Test Todo 2")
        response = self.client.get(self.url)
        self.assertContains(response, "Test Todo 1")
        self.assertContains(response, "Test Todo 2")
    
    def test_list_view_ordering(self):
        """Test that todos are displayed in correct order"""
        todo1 = Todo.objects.create(title="Resolved", is_resolved=True)
        todo2 = Todo.objects.create(title="Unresolved", is_resolved=False)
        response = self.client.get(self.url)
        
        # Get the order of todos in the response
        content = response.content.decode()
        pos_unresolved = content.find("Unresolved")
        pos_resolved = content.find("Resolved")
        
        # Unresolved should appear before resolved
        self.assertLess(pos_unresolved, pos_resolved)


class TodoDetailViewTest(TestCase):
    """Tests for the Todo detail view"""
    
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(title="Test Todo", description="Test Description")
        self.url = reverse('todo-detail', args=[self.todo.pk])
    
    def test_detail_view_status_code(self):
        """Test that detail view returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_detail_view_template(self):
        """Test correct template is used"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todos/todo_detail.html')
    
    def test_detail_view_404_for_nonexistent(self):
        """Test 404 for non-existent todo"""
        url = reverse('todo-detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_detail_view_contains_todo_data(self):
        """Test that todo data is displayed"""
        response = self.client.get(self.url)
        self.assertContains(response, "Test Todo")
        self.assertContains(response, "Test Description")


class TodoCreateViewTest(TestCase):
    """Tests for the Todo create view"""
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('todo-create')
    
    def test_create_view_get(self):
        """Test GET request renders form"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_form.html')
    
    def test_create_view_post_valid_data(self):
        """Test POST with valid data creates todo"""
        data = {
            'title': 'New Todo',
            'description': 'New Description',
            'due_date': date.today(),
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 1)
        todo = Todo.objects.first()
        self.assertEqual(todo.title, 'New Todo')
    
    def test_create_view_redirect(self):
        """Test redirect after successful creation"""
        data = {'title': 'New Todo'}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('todo-list'))
    
    def test_create_view_form_validation_errors(self):
        """Test that form validation errors are displayed"""
        data = {}  # Missing required title
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIn('title', response.context['form'].errors)


class TodoUpdateViewTest(TestCase):
    """Tests for the Todo update view"""
    
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(title="Original Title")
        self.url = reverse('todo-edit', args=[self.todo.pk])
    
    def test_update_view_get(self):
        """Test GET request renders form with existing data"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Original Title")
    
    def test_update_view_post_valid_data(self):
        """Test POST with valid data updates todo"""
        data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'is_resolved': True
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Title')
        self.assertTrue(self.todo.is_resolved)
    
    def test_update_view_redirect(self):
        """Test redirect after successful update"""
        data = {'title': 'Updated Title'}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('todo-list'))
    
    def test_update_view_404_for_nonexistent(self):
        """Test 404 for non-existent todo"""
        url = reverse('todo-edit', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TodoDeleteViewTest(TestCase):
    """Tests for the Todo delete view"""
    
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(title="To Delete")
        self.url = reverse('todo-delete', args=[self.todo.pk])
    
    def test_delete_view_get(self):
        """Test GET request renders confirmation page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_confirm_delete.html')
    
    def test_delete_view_post(self):
        """Test POST deletes todo"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 0)
    
    def test_delete_view_redirect(self):
        """Test redirect after deletion"""
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('todo-list'))


class TodoToggleResolvedTest(TestCase):
    """Tests for the toggle resolved functionality"""
    
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(title="Test Todo", is_resolved=False)
        self.url = reverse('todo-toggle-resolved', args=[self.todo.pk])
    
    def test_toggle_resolved_post(self):
        """Test POST toggles is_resolved status"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.is_resolved)
        
        # Toggle again
        response = self.client.post(self.url)
        self.todo.refresh_from_db()
        self.assertFalse(self.todo.is_resolved)
    
    def test_toggle_resolved_redirect(self):
        """Test redirect to list view"""
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('todo-list'))
    
    def test_toggle_resolved_only_post(self):
        """Test that only POST method is accepted"""
        response = self.client.get(self.url)
        # Should not be allowed (405 Method Not Allowed or redirect)
        self.assertNotEqual(response.status_code, 200)


class TodoIntegrationTest(TestCase):
    """Integration tests for full CRUD workflows"""
    
    def setUp(self):
        self.client = Client()
    
    def test_full_crud_workflow(self):
        """Test complete CRUD workflow: Create → Read → Update → Delete"""
        # Create
        create_data = {
            'title': 'Integration Test Todo',
            'description': 'Test Description',
            'due_date': date.today() + timedelta(days=7)
        }
        response = self.client.post(reverse('todo-create'), create_data)
        self.assertEqual(response.status_code, 302)
        
        # Read (List)
        response = self.client.get(reverse('todo-list'))
        self.assertContains(response, 'Integration Test Todo')
        
        # Read (Detail)
        todo = Todo.objects.first()
        response = self.client.get(reverse('todo-detail', args=[todo.pk]))
        self.assertContains(response, 'Integration Test Todo')
        
        # Update
        update_data = {
            'title': 'Updated Integration Test',
            'description': 'Updated Description',
            'is_resolved': True
        }
        response = self.client.post(reverse('todo-edit', args=[todo.pk]), update_data)
        self.assertEqual(response.status_code, 302)
        todo.refresh_from_db()
        self.assertEqual(todo.title, 'Updated Integration Test')
        
        # Delete
        response = self.client.post(reverse('todo-delete', args=[todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 0)
    
    def test_toggle_resolved_workflow(self):
        """Test create → toggle resolved → verify status"""
        # Create todo
        todo = Todo.objects.create(title="Test Todo", is_resolved=False)
        
        # Toggle to resolved
        response = self.client.post(reverse('todo-toggle-resolved', args=[todo.pk]))
        todo.refresh_from_db()
        self.assertTrue(todo.is_resolved)
        
        # Verify in list view
        response = self.client.get(reverse('todo-list'))
        self.assertContains(response, "Test Todo")
    
    def test_multiple_todos_different_states(self):
        """Test handling multiple todos with different states"""
        # Create multiple todos
        Todo.objects.create(title="Todo 1", is_resolved=False)
        Todo.objects.create(title="Todo 2", is_resolved=True)
        Todo.objects.create(title="Todo 3", is_resolved=False, due_date=date.today())
        
        # Verify all appear in list
        response = self.client.get(reverse('todo-list'))
        self.assertContains(response, "Todo 1")
        self.assertContains(response, "Todo 2")
        self.assertContains(response, "Todo 3")
        
        # Verify count
        self.assertEqual(Todo.objects.count(), 3)
