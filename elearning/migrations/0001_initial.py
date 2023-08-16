# Generated by Django 4.2.4 on 2023-08-16 13:42

import uuid

import django.contrib.postgres.fields
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
                ("index", models.IntegerField()),
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
                ("index", models.IntegerField()),
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
                ("index", models.IntegerField()),
                ("duration", models.IntegerField()),
                (
                    "complexity",
                    models.CharField(
                        choices=[("1", "Low"), ("2", "Medium"), ("3", "High")],
                        default="1",
                        max_length=1,
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
                ("name", models.CharField(max_length=100, verbose_name="label")),
                (
                    "path",
                    models.FilePathField(
                        path="/home/cases/eLearning/theme/static/", recursive=True
                    ),
                ),
                (
                    "m_type",
                    models.CharField(
                        choices=[("1", "Image"), ("2", "Video"), ("3", "Audio")],
                        default="1",
                        max_length=1,
                        verbose_name="type",
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
                ("index", models.IntegerField()),
                ("score", models.IntegerField(default=0)),
                ("is_correct", models.BooleanField(default=False)),
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
                        verbose_name="type",
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
                    "level",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elearning.level",
                    ),
                ),
            ],
            options={
                "verbose_name": "Question",
                "verbose_name_plural": "Questions",
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Resource",
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
                    "level",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elearning.level",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ressource",
                "verbose_name_plural": "Ressources",
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="User",
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
                            ("1", "Not started"),
                            ("2", "In progress"),
                            ("3", "Finished"),
                        ],
                        default="1",
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
                "verbose_name": "Users",
                "verbose_name_plural": "Users",
            },
        ),
        migrations.CreateModel(
            name="QuestionMediaTemplate",
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
                (
                    "css_classes",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(blank=True, max_length=50),
                        default=list,
                        size=None,
                    ),
                ),
                (
                    "media",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elearning.media",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elearning.question",
                    ),
                ),
            ],
            options={
                "verbose_name": "Media Template",
                "verbose_name_plural": "Media Templates",
            },
        ),
        migrations.AddField(
            model_name="question",
            name="medias",
            field=models.ManyToManyField(
                through="elearning.QuestionMediaTemplate", to="elearning.media"
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="options",
            field=models.ManyToManyField(to="elearning.option"),
        ),
        migrations.CreateModel(
            name="ContextMediaTemplate",
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
                (
                    "css_classes",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(blank=True, max_length=50),
                        default=list,
                        size=None,
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
                    "media",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elearning.media",
                    ),
                ),
            ],
            options={
                "verbose_name": "Media Template",
                "verbose_name_plural": "Media Templates",
            },
        ),
        migrations.AddField(
            model_name="context",
            name="medias",
            field=models.ManyToManyField(
                through="elearning.ContextMediaTemplate", to="elearning.media"
            ),
        ),
        migrations.AddField(
            model_name="context",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="elearning.question"
            ),
        ),
        migrations.CreateModel(
            name="Challenge",
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
                    "level",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elearning.level",
                    ),
                ),
            ],
            options={
                "verbose_name": "Challenge",
                "verbose_name_plural": "Challenges",
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name="category",
            name="level",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="elearning.level"
            ),
        ),
        migrations.CreateModel(
            name="Answer",
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
                ("option", models.ManyToManyField(to="elearning.option")),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elearning.question",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="elearning.user"
                    ),
                ),
            ],
            options={
                "verbose_name": "Answer",
                "verbose_name_plural": "Answers",
            },
        ),
        migrations.CreateModel(
            name="ResourceTranslation",
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
                ("name", models.CharField(max_length=100, verbose_name="label")),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="elearning.resource",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ressource Translation",
                "db_table": "elearning_resource_translation",
                "db_tablespace": "",
                "managed": True,
                "default_permissions": (),
                "unique_together": {("language_code", "master")},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
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
                ("name", models.TextField(verbose_name="label")),
                ("explanation", models.TextField()),
                ("tooltip", models.TextField(blank=True, default=None, null=True)),
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
                ("name", models.TextField(verbose_name="label")),
                ("tooltip", models.TextField(blank=True, default=None, null=True)),
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
                ("name", models.CharField(max_length=100, verbose_name="label")),
                ("plot", models.TextField()),
                ("objectives", models.TextField()),
                ("requirements", models.TextField()),
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
                ("name", models.TextField(verbose_name="Title")),
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
            name="ChallengeTranslation",
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
                ("name", models.TextField(verbose_name="description")),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="elearning.challenge",
                    ),
                ),
            ],
            options={
                "verbose_name": "Challenge Translation",
                "db_table": "elearning_challenge_translation",
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
                ("name", models.CharField(max_length=100, verbose_name="label")),
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