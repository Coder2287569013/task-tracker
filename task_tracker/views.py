from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .forms import TaskForm
from .models import Task
# Create your views here.

class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'


class TaskDetailView(DetailView):
    model = Task
    context_object_name = 'task'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task-list')