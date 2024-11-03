# from django.forms import BaseModelForm
# from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import TaskForm, TaskFilterForm, CommentForm
from .models import Like, Task, Comment
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
        comment_form = CommentForm(request.POST, request.FILES)
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

class CommentDeleteView(UserIsOwnerMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        task = self.object.task
        return reverse_lazy('task-detail', kwargs={'pk': task.pk})
    

class CommentLikeToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        like_q = Like.objects.filter(comment=comment, user=request.user)
        if like_q.exists():
            like_q.delete()
        else:
            Like.objects.create(comment=comment, user=request.user)
        
        return HttpResponseRedirect(comment.get_absolute_url())


class CustomLoginView(LoginView):
    template_name = 'task_tracker/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = 'login'


# class RegisterView(CreateView):
#     model = User
#     template_name = "task_tracker/register.html"
#     form = UserCreationForm
#     # success_url = reverse_lazy('task-list')

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)

#         return redirect('task-list')

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("task-list")
    else:
        form = UserCreationForm()

    return render(
        request,           
        "task_tracker/register_form.html", 
        {"form": form}
    )