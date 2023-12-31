# Generated by Django 4.2.6 on 2023-10-25 12:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("elearning", "0006_resourcetype_resource_resourcetype_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="current_level",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="elearning.level",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="current_question",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="elearning.question",
            ),
        ),
    ]
