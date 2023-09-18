# Generated by Django 4.2.4 on 2023-08-24 07:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("elearning", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="resource",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="elearning.category",
            ),
        ),
        migrations.AddField(
            model_name="resource",
            name="path",
            field=models.FilePathField(
                default=None,
                path="/home/cases/eLearning/theme/static/media",
                recursive=True,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="resourcetranslation",
            name="description",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="challenge",
            name="level",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="elearning.level",
            ),
        ),
        migrations.AlterField(
            model_name="context",
            name="question",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="elearning.question",
            ),
        ),
        migrations.AlterField(
            model_name="media",
            name="m_type",
            field=models.CharField(
                choices=[
                    ("1", "Image"),
                    ("2", "Video"),
                    ("3", "Audio"),
                    ("4", "Document"),
                ],
                default="1",
                max_length=1,
                verbose_name="type",
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
            name="level",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="elearning.level",
            ),
        ),
    ]