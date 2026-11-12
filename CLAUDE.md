# CLAUDE.md — ALTO E-Learning Platform

## Project Overview

ALTO is NC3-LU's open-source e-learning platform. It provides course authoring,
interactive questions and quizzes, learner progress tracking, statistics, resource
downloads, and PDF reports and certificates.

The repository is a Django monolith with a single application, `elearning`. Course
content is managed through the Django admin. The learner-facing templates and static
assets live in a separate, gitignored repository checked out as `theme/`.

There are two distinct user concepts:

- `django.contrib.auth.models.User` is used for administrators and protected statistics.
- `elearning.models.User` represents a learner. It is identified by a UUID stored in the
  session and does not have a Django authentication account.

Do not confuse these models when changing authentication, permissions, statistics, or
course progress.

## Tech Stack

| Layer | Technology | Declared version |
|-------|------------|------------------|
| Language | Python | `>=3.12,<4` |
| Framework | Django | `>=6.0,<7` |
| Database | PostgreSQL | required |
| Package manager | Poetry | lock file committed |
| Translations | django-parler | `>=2.3,<3` |
| Admin data exchange | django-import-export | `>=3.2,<4` |
| PDF generation | WeasyPrint | `>=61.1,<62` |
| Frontend | Bootstrap 5, jQuery, Chart.js | npm-managed |
| Node.js / npm | Node 20 / npm 10.8 | from `package.json` |
| Formatting | Black + isort | pre-commit |
| Linting | flake8 | pre-commit and CI |
| Documentation | Sphinx | `docs/` |

PostgreSQL is not interchangeable with SQLite without code changes because models use
`django.contrib.postgres.fields.ArrayField`.

## Build and Run

Keep the Poetry environment local to this repository. Before running Poetry, deactivate
any virtual environment belonging to another project.

```bash
poetry config virtualenvs.in-project true --local
poetry env use python3.13       # or another supported interpreter
poetry install
npm install
```

The expected interpreter is `<repository>/.venv/bin/python`. Verify it when environment
selection is in doubt:

```bash
poetry env info
poetry run which python
poetry run python --version
```

Create the local configuration and adjust the database connection and secrets:

```bash
cp elearning/config_dev.py elearning/config.py
poetry run python manage.py migrate
poetry run python manage.py collectstatic
poetry run python manage.py compilemessages
poetry run python manage.py runserver 127.0.0.1:8000
```

`elearning/config.py` is gitignored and must never be committed.

The PostgreSQL role configured in `DATABASES` must own the development database and its
schema objects. A connection that succeeds but cannot read `django_migrations` indicates
a database ownership/privilege problem, not a Django dependency problem.

## Configuration

`elearning/settings.py` imports `elearning/config.py`. When it does not exist, settings
fall back to `elearning/config_dev.py`.

Configuration values consumed by settings include:

- `SECRET_KEY` and `HASH_KEY`
- `DEBUG`
- `DATABASES`
- `PUBLIC_URL`, `ALLOWED_HOSTS`, and `SITE_NAME`
- `MEDIA_DIR`
- `LOGGING` and `LOG_DIRECTORY`
- `ALLOW_ANONYMOUS_STATS_ACCESS`
- `SATISFACTION_SURVEY_URL`
- `LANGUAGE_CODE`, `LANGUAGES`, `PARLER_DEFAULT_LANGUAGE_CODE`, and `PARLER_LANGUAGES`
- cookie and session settings
- `PRESHARED_SURVEY_KEY`
- optional CORS origins, regular expressions, and methods

Never copy development secrets into production. Production must use a new Django secret
key and Fernet-compatible hash key, `DEBUG = False`, secure cookies, appropriate hosts,
and production database credentials.

## Project Structure

```text
elearning/
  admin.py          Course authoring admin and import/export resources
  models.py         Course content, learner progress, answers, and scores
  views.py          HTTP endpoints and response handling
  viewLogic.py      Course sequencing, scoring, resources, and PDF generation
  forms.py          Dynamic answer forms and resource download forms
  decorators.py     Learner UUID, template, and statistics access guards
  globals.py        Question, media, text, and layout choices
  mixins.py         Translation-aware import behaviour
  widgets.py        Admin import/export and answer widgets
  settings.py       Django settings loaded from config.py/config_dev.py
  urls.py           All application URL routes
  migrations/       Append-only database migrations
  templates/        App-owned widget templates only

theme/              Separate git repository: templates, static files, locale, seed data
locale/             Application translations (French and German)
docs/               Sphinx installation and operating documentation
scripts/            Update, data dump, and data load scripts
docker/             Web, Nginx, PostgreSQL 18, and Compose configuration
```

## Domain Model and Course Flow

Content models such as `Level`, `Category`, `AnswerChoice`, `Text`, `Resource`,
`Question`, `Explanation`, `Quiz`, and `Context` use django-parler where fields are
translated.

`LevelSequence` orders course slides by level and position. It uses Django content types
and a `GenericForeignKey` so a sequence entry can point to different course-content
models. Preserve both the ordering and content-type relationship when changing course
navigation.

Several many-to-many relationships use explicit through models because they carry
ordering, correctness, position, or CSS metadata:

- `QuestionAnswerChoice` stores answer order and correctness.
- `QuizQuestion` stores question order and quiz-label display behaviour.
- context, question, and explanation template models store layout positions and CSS
  classes.

Learner state is split across:

- `User.current_level` and `User.current_position`
- `Answer` for selected answer choices
- `Score` for per-level score and progress
- `Knowledge` for progress by category

The logic that updates this state is concentrated in `viewLogic.py`. Reuse those
functions rather than duplicating scoring or navigation rules in views.

Question types are defined in `elearning/globals.py`. `AnswerForm` maps each type to a
specific form field and widget. A new question type therefore requires coordinated
changes to the choices, form construction, scoring, course rendering, statistics, admin,
and theme templates.

## Learner Sessions and Access

Learners are resumed through their UUID. `user_uuid_required` validates the UUID stored
in the session before protected course endpoints run. Treat a learner UUID as a sensitive
access token:

- do not expose UUIDs unnecessarily;
- do not log them with answers, scores, or reports;
- validate external UUID values before querying;
- retain `user_uuid_required` on learner-specific views;
- always scope answers, scores, resources, reports, and certificates to the current
  learner.

The statistics view is public only when `ALLOW_ANONYMOUS_STATS_ACCESS` is true. Otherwise
`stats_login_required` requires an authenticated Django user. Do not weaken that boundary
implicitly.

## Theme and Frontend

Almost all rendered pages and static assets come from the separate repository at
`theme/`. The current checkout uses the `NC3-LU/daaz_theme` repository. The directory is
ignored by the main repository and has its own Git history.

When changing templates, CSS, JavaScript, images, PDF layouts, or theme translations:

1. Check `theme/` first; it usually owns the rendered asset.
2. Make and review the change inside the theme repository.
3. Commit theme changes from `theme/`, not from the ALTO repository.
4. Keep backend expectations and theme templates compatible.

The theme also has its own `theme/docker/Dockerfile`. The Docker Compose
stack builds it separately and shares its content with the web container
through the `theme_data` volume. See `docker/README.md` before changing
the Docker theme update workflow.

Root `npm install` creates `static/npm_components` as a link to `node_modules`. Compile
theme SCSS with:

```bash
npm run compile-scss
```

Missing `static/` or `theme/static/` warnings mean frontend assets have not been fully
prepared. They are separate from Python dependency failures.

## Translations

Translated model fields use `TranslatableModel` and `TranslatedFields`. The configured
languages are defined in `config.py`; the development defaults are English, French, and
German.

When creating translated data in code or fixtures, set the object's current language
before assigning translated fields. Admin import/export behaviour is implemented by
`TranslationImportMixin` and the custom widgets in `widgets.py`.

Application message catalogs live under `locale/`; theme catalogs live under
`theme/locale/`.

```bash
poetry run python manage.py makemessages -a
poetry run python manage.py compilemessages
```

Do not edit compiled `.mo` files; they are generated and gitignored.

## PDF Reports and Certificates

`viewLogic.py` renders reports and certificates with WeasyPrint using theme templates and
CSS from `theme/static`. Changes to these PDFs may span backend context, theme HTML, and
theme CSS. Verify both report and certificate generation after such changes.

Resource and media paths are stored with `FilePathField` and are rooted in `MEDIA_DIR`.
Do not accept arbitrary filesystem paths from requests or bypass the database-backed
resource selection.

## Admin and Data Import/Export

The custom `AdminSite` is defined in `elearning/admin.py`. Course content is maintained
there with django-import-export and translated admin classes.

Imports must preserve translated fields and explicit through-model metadata. Extend the
existing resource classes and widgets when changing import/export behaviour rather than
creating a second import path.

Seed content is stored in the theme repository under `theme/data`. Use the provided
scripts from the ALTO repository root:

```bash
./scripts/load_data.sh
./scripts/dump_data.sh
```

The dump intentionally excludes learner answers, knowledge, scores, and users.

## API

There is currently no application API. DRF Spectacular and its sidecar are installed,
but `urls.py` defines ordinary Django views only; there are no serializers, viewsets, or
API routers. Adding an API is an architectural change and requires explicit approval.

## Database and Migrations

- Use the Django ORM instead of raw SQL in application code.
- Avoid N+1 queries with `select_related`, `prefetch_related`, annotations, and aggregates.
- Migrations are append-only. Never modify the committed `0001_initial.py`; create a new
  migration.
- Do not make schema changes unless the task requires them.
- Keep migrations compatible with PostgreSQL-specific fields and content types.
- Test generic relationships and translated models carefully when changing model links.

```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py makemigrations --check --dry-run
```

## Tests and Verification

The repository currently has no automated Django test suite. New behaviour should add
focused tests under `elearning/tests/` using Django's test framework unless the project
adopts another established test layout first.

Run checks appropriate to the change:

```bash
poetry run python manage.py check
poetry run python manage.py test
poetry run black --check elearning manage.py
poetry run isort --check-only elearning manage.py
poetry run flake8 . --count --max-complexity=36 --max-line-length=140 --statistics
poetry run pre-commit run --all-files
```

Database-backed commands require a running PostgreSQL server with correct ownership and
permissions. PDF tests also require the native libraries used by WeasyPrint and a complete
theme checkout.

CI runs flake8 on pushes and CodeQL on `master`. Local validation should not be weaker
than the checks relevant to the files changed.

## Code Style and Change Discipline

- Understand the existing implementation and search for an established pattern first.
- Prefer small changes to existing files over new abstractions.
- Keep HTTP handling in `views.py` and course calculations/state transitions in
  `viewLogic.py` unless a broader refactor is explicitly approved.
- Preserve existing public URLs, model fields, import formats, and theme contracts unless
  the task requires a change.
- Use Black-compatible formatting and isort-compatible imports.
- Do not rename legacy modules such as `viewLogic.py` as incidental cleanup.
- Do not edit generated files, compiled translations, or old migrations.
- Do not add dependencies without a concrete need and an updated lock file.
- Do not commit `elearning/config.py`, secrets, local logs, generated emails, collected
  static files, `node_modules`, `.venv`, or the `theme/` checkout.

## Changelog

`CHANGELOG.md` lives at the repo root and follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format.

**Every PR that ships user-facing changes must include a `CHANGELOG.md` update.**

Rules:
- Add entries under `## [Unreleased]` — never edit a released version's section.
- Use the correct category: `Added` (new feature), `Changed` (behaviour change), `Fixed` (bug fix).
- Reference the GitHub issue number where one exists, e.g. `Fixed: foo bar (#123)`.
- When a version is released, rename `[Unreleased]` to `[X.Y.Z] - YYYY-MM-DD` and add a fresh empty `[Unreleased]` block above it. Also add the comparison link at the bottom of the file.
- Omit pure chore entries (dependency bumps, translation updates, theme submodule bumps) unless they affect end-users.

## Security

- Treat request data, imported data, UUIDs, and resource selections as untrusted.
- Keep Django CSRF, template escaping, authentication, and clickjacking protections
  enabled.
- Never use `mark_safe` for user-controlled content without sanitisation.
- Never put secrets, database passwords, learner UUIDs, answers, or scores in logs.
- Use ORM parameterisation and avoid raw SQL.
- Keep production cookies secure and disable debug mode.
- Scope every learner-data query to the learner resolved from the validated session UUID.
- Preserve authentication on the admin and on statistics when anonymous access is
  disabled.

## Documentation

Sphinx documentation lives in `docs/`. Update the relevant page when installation,
configuration, update procedures, database setup, or operator workflows change.

```bash
poetry run sphinx-build -b html docs docs/_build/html
```

Documentation examples must use `poetry run python manage.py ...` and must not include
real credentials or production secrets.
