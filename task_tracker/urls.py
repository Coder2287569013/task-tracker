from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task-list'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('task-form/', views.TaskCreateView.as_view(), name='task-form'),
    path('task-update/<int:pk>/', views.TaskUpdateView.as_view(), name='task-update'),
    path('comment-update/<int:pk>/', views.CommentUpdateView.as_view(), name="comment-update"),
    path('comment-delete/<int:pk>/', views.CommentDeleteView.as_view(), name="comment-delete"),
    path('comment/like/<int:pk>/', views.CommentLikeToggle.as_view(), name='comment-toggle-like'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register')
]
