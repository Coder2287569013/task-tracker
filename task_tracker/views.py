# from django.forms import BaseModelForm
# from django.http import HttpResponse
# from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TaskForm, TaskFilterForm
from .models import Task
from .mixins import UserIsOwnerMixin
# Create your views here.

class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        query_set = super().get_queryset()
        status = self.request.GET.get('status', '')
        if status:
            query_set = query_set.filter(status=status)
        
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskFilterForm(self.request.GET)

        return context

class TaskDetailView(DetailView):
    model = Task
    context_object_name = 'task'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task-list')

