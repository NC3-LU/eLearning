# Generated by Django 4.2.4 on 2023-08-24 08:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("elearning", "0003_alter_resource_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resourcetranslation",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]
