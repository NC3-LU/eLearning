# Generated by Django 4.2.6 on 2023-10-31 08:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("elearning", "0016_remove_category_level_remove_context_index_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="challenge",
            name="level",
        ),
    ]