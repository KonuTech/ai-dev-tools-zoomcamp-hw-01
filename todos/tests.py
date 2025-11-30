from django.test import TestCase, Client
from django.urls import reverse
from todos.models import Todo

class TodoModelTest(TestCase):
    def test_string_representation(self):
        todo = Todo(title="Test Todo")
        self.assertEqual(str(todo), "Test Todo")

    def test_default_values(self):
        todo = Todo.objects.create(title="Test Todo")
        self.assertFalse(todo.is_resolved)
        self.assertIsNone(todo.due_date)

class TodoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(title="Test Todo")

    def test_todo_list_view(self):
        response = self.client.get(reverse('todo-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Todo")

    def test_todo_detail_view(self):
        response = self.client.get(reverse('todo-detail', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Todo")

    def test_todo_create_view(self):
        response = self.client.post(reverse('todo-create'), {
            'title': 'New Todo',
            'description': 'Description'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 2)

    def test_todo_update_view(self):
        response = self.client.post(reverse('todo-edit', args=[self.todo.pk]), {
            'title': 'Updated Todo',
            'description': 'Updated Description',
            'is_resolved': True
        })
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Todo')
        self.assertTrue(self.todo.is_resolved)

    def test_todo_delete_view(self):
        response = self.client.post(reverse('todo-delete', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 0)
