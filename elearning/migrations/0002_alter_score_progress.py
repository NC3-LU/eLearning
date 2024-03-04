# Generated by Django 4.2.7 on 2024-03-04 12:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("elearning", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="score",
            name="progress",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=5,
                validators=[django.core.validators.MaxValueValidator(100)],
            ),
        ),
    ]
