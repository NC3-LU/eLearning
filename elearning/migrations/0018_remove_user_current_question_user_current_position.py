# Generated by Django 4.2.6 on 2023-10-31 10:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("elearning", "0017_remove_challenge_level"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="current_question",
        ),
        migrations.AddField(
            model_name="user",
            name="current_position",
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
