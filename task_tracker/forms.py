from django.forms.models import ModelForm
from django import forms
from .models import Task

class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
  
        self.fields["due_date"].widget = forms.DateTimeInput(attrs={"type": "datetime-local"})

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']
