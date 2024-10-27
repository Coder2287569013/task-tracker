# from django.forms import BaseModelForm
# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TaskForm, TaskFilterForm, CommentForm
from .models import Task, Comment
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

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()

        return context
    
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.creator = request.user
            comment.task = self.get_object()
            comment.save()
            return redirect('task-detail', pk=comment.task.pk)


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

class CommentUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    
    def get_success_url(self):
        task = self.object.task
        return reverse_lazy('task-detail', kwargs={'pk': task.pk})