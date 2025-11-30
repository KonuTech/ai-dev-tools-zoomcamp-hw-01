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
