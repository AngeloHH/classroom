# Generated by Django 4.2 on 2023-05-11 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0002_assignment_remove_exercise_answers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='points',
            field=models.FloatField(default=0),
        ),
    ]