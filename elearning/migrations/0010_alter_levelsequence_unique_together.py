# Generated by Django 4.2.6 on 2023-10-30 09:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("elearning", "0009_levelsequence"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="levelsequence",
            unique_together={("level", "position")},
        ),
    ]
