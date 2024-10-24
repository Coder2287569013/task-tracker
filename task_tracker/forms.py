from django import forms
from .models import Task, Comment

class TaskForm(forms.models.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
  
        self.fields["due_date"].widget = forms.DateTimeInput(attrs={"type": "datetime-local"})

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']


class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', 'all'),
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label='status')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']