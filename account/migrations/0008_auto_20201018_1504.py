# Generated by Django 3.0 on 2020-10-18 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20201018_1503'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='is_teacher',
        ),
        migrations.AddField(
            model_name='student',
            name='is_student',
            field=models.BooleanField(default=True),
        ),
    ]
