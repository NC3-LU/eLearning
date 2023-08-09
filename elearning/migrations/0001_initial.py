# Generated by Django 4.2.4 on 2023-08-09 10:03

import uuid

import django.db.models.deletion
import parler.fields
import parler.models
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Context",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "Context",
                "verbose_name_plural": "Contexts",
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Level",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "Level",
                "verbose_name_plural": "Levels",
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Media",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("path", models.CharField(max_length=100)),
                (
                    "position",
                    models.CharField(
                        choices=[
                            ("TL", "Top Left"),
                            ("TC", "Top Center"),
                            ("TR", "Top Right"),
                            ("ML", "Middle Left"),
                            ("MC", "Middle Center"),
                            ("MR", "Middle Right"),
                            ("BL", "Bottom Left"),
                            ("BC", "Bottom Center"),
                            ("BR", "Bottom Right "),
                        ],
                        default="TL",
                        max_length=2,
                    ),
                ),
            ],
            options={
                "verbose_name": "Media",
                "verbose_name_plural": "Medias",
            },
        ),
        migrations.CreateModel(
            name="Option",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("index", models.IntegerField(unique=True)),
                ("score", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name": "Option",
                "verbose_name_plural": "Options",
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("index", models.IntegerField(unique=True)),
                (
                    "q_type",
                    models.CharField(
                        choices=[
                            ("M", "Multiple Choice"),
                            ("S", "Single Choice"),
                            ("SO", "Single Option Choice"),
                            ("T", "Free text"),
                            ("MT", "Multiple Choice + Free Text"),
                            ("ST", "Single Choice + Free Text"),
                            ("CL", "Countries list"),
                        ],
                        default="M",
                        max_length=2,
                    ),
                ),
                ("max_score", models.IntegerField(default=100)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elearning.category",
                    ),
                ),
                (
                    "context",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elearning.context",
                    ),
                ),
                (
                    "level",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elearning.level",
                    ),
                ),
                ("media", models.ManyToManyField(to="elearning.media")),
                ("options", models.ManyToManyField(to="elearning.option")),
            ],
            options={
                "verbose_name": "Question",
                "verbose_name_plural": "Questions",
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="learner",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                (
                    "status_level",
                    models.CharField(
                        choices=[
                            (1, "Not started"),
                            (2, "In progress"),
                            (3, "Finished"),
                        ],
                        default=1,
                        max_length=1,
                    ),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                (
                    "current_level",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elearning.level",
                    ),
                ),
                (
                    "current_question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elearning.question",
                    ),
                ),
            ],
            options={
                "verbose_name": "Learner",
                "verbose_name_plural": "Learners",
            },
        ),
        migrations.AddField(
            model_name="context",
            name="media",
            field=models.ManyToManyField(to="elearning.media"),
        ),
        migrations.CreateModel(
            name="answer",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "learner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elearning.learner",
                    ),
                ),
                ("option", models.ManyToManyField(to="elearning.option")),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elearning.question",
                    ),
                ),
            ],
            options={
                "verbose_name": "Answer",
                "verbose_name_plural": "Answers",
            },
        ),
        migrations.CreateModel(
            name="QuestionTranslation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "language_code",
                    models.CharField(
                        db_index=True, max_length=15, verbose_name="Language"
                    ),
                ),
                ("name", models.TextField()),
                ("tooltip", models.TextField(blank=True, default="")),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="elearning.question",
                    ),
                ),
            ],
            options={
                "verbose_name": "Question Translation",
                "db_table": "elearning_question_translation",
                "db_tablespace": "",
                "managed": True,
                "default_permissions": (),
                "unique_together": {("language_code", "master")},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="OptionTranslation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "language_code",
                    models.CharField(
                        db_index=True, max_length=15, verbose_name="Language"
                    ),
                ),
                ("name", models.TextField()),
                ("tooltip", models.TextField(blank=True, default="")),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="elearning.option",
                    ),
                ),
            ],
            options={
                "verbose_name": "Option Translation",
                "db_table": "elearning_option_translation",
                "db_tablespace": "",
                "managed": True,
                "default_permissions": (),
                "unique_together": {("language_code", "master")},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="LevelTranslation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "language_code",
                    models.CharField(
                        db_index=True, max_length=15, verbose_name="Language"
                    ),
                ),
                ("name", models.TextField()),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="elearning.level",
                    ),
                ),
            ],
            options={
                "verbose_name": "Level Translation",
                "db_table": "elearning_level_translation",
                "db_tablespace": "",
                "managed": True,
                "default_permissions": (),
                "unique_together": {("language_code", "master")},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="ContextTranslation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "language_code",
                    models.CharField(
                        db_index=True, max_length=15, verbose_name="Language"
                    ),
                ),
                ("name", models.TextField()),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="elearning.context",
                    ),
                ),
            ],
            options={
                "verbose_name": "Context Translation",
                "db_table": "elearning_context_translation",
                "db_tablespace": "",
                "managed": True,
                "default_permissions": (),
                "unique_together": {("language_code", "master")},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="CategoryTranslation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "language_code",
                    models.CharField(
                        db_index=True, max_length=15, verbose_name="Language"
                    ),
                ),
                ("name", models.TextField()),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="elearning.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category Translation",
                "db_table": "elearning_category_translation",
                "db_tablespace": "",
                "managed": True,
                "default_permissions": (),
                "unique_together": {("language_code", "master")},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
