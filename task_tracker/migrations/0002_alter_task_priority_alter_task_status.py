# Generated by Django 5.1.1 on 2024-10-13 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('Low', 'low'), ('Medium', 'medium'), ('High', 'high')], default='medium', max_length=20),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('To Do', 'todo'), ('In Progress', 'in_progress'), ('Done', 'done')], default='todo', max_length=20),
        ),
    ]
