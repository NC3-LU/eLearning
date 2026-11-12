# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Raised the minimum supported Python version from 3.10 to 3.12 and upgraded Django from 4.2 to the `>=6.0,<7` release line, currently locked at Django 6.1.3.
- Updated the Django ecosystem packages, including django-bootstrap5, django-cors-headers, django-debug-toolbar, django-formtools, django-import-export, django-parler, DRF Spectacular, and WeasyPrint.
- Migrated application settings, custom widgets, and admin import/export resources to their supported Django 6 and package APIs.
- Added a migration preserving translated-model uniqueness constraints with django-parler 2.4.
- Updated CI, pre-commit checks, installation documentation, and project instructions for Python 3.12+ and Django 6.

### Fixed

- Restored page rendering with django-bootstrap5 26 by updating the theme's Bootstrap setting usage.
- Replaced the removed Django `length_is` template filter in generated report templates.

[Unreleased]: https://github.com/NC3-LU/eLearning/compare/v1.0.0...HEAD
