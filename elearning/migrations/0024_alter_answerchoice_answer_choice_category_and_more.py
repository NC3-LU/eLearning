# Generated by Django 4.2.7 on 2023-11-20 08:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("elearning", "0023_answerchoicecategory_answerchoice_answer_text_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answerchoice",
            name="answer_choice_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="elearning.answerchoicecategory",
            ),
        ),
        migrations.AlterField(
            model_name="media",
            name="path",
            field=models.FilePathField(
                path="/home/cases/eLearning/theme/static/media", recursive=True
            ),
        ),
        migrations.AlterField(
            model_name="resource",
            name="path",
            field=models.FilePathField(
                path="/home/cases/eLearning/theme/static/media", recursive=True
            ),
        ),
    ]
