# Generated by Django 4.2.4 on 2023-08-24 07:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("elearning", "0002_resource_category_resource_path_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="resource",
            options={"verbose_name": "Resource", "verbose_name_plural": "Resources"},
        ),
        migrations.AlterModelOptions(
            name="resourcetranslation",
            options={
                "default_permissions": (),
                "managed": True,
                "verbose_name": "Resource Translation",
            },
        ),
        migrations.AlterField(
            model_name="categorytranslation",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]
