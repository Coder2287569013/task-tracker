from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task-list'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('task-form/', views.TaskCreateView.as_view(), name='task-form'),
    path('task-update/<int:pk>', views.TaskUpdateView.as_view(), name='task-update')
]
