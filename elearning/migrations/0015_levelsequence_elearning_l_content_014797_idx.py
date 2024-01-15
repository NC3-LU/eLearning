# Generated by Django 4.2.6 on 2023-10-31 08:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("elearning", "0014_remove_user_status_level"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="levelsequence",
            index=models.Index(
                fields=["content_type", "object_id"],
                name="elearning_l_content_014797_idx",
            ),
        ),
    ]