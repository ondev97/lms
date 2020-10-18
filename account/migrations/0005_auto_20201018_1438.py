# Generated by Django 3.0 on 2020-10-18 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='is_student',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='is_teacher',
        ),
        migrations.AddField(
            model_name='student',
            name='role',
            field=models.CharField(default='student', max_length=10),
        ),
        migrations.AddField(
            model_name='teacher',
            name='role',
            field=models.CharField(default='teacher', max_length=10),
        ),
    ]
