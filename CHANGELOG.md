# Changelog

## 1.0.0 - 2026-11-27

First tagged release: the 2018 Django Girls tutorial app, updated for current Django.

- Upgrade from Django 1.11 to Django 6.1.3; requires Python 3.12 or newer.
- Replace `url()` routes with `path()`, use `pathlib` paths in settings and drop the removed
  `USE_L10N` setting.
- Set `DEFAULT_AUTO_FIELD` to `AutoField` so the existing migration still matches the model
  (no schema change).
- Read `DEBUG`, `SECRET_KEY` and `ALLOWED_HOSTS` from environment variables with development
  defaults; refuse to start with `DEBUG` off and no secret key. Optional HTTPS hardening
  (`DJANGO_HTTPS`) so `manage.py check --deploy` passes for a production configuration.
- Add tests for the `Post` model, the post list page and the admin.
- Add pinned `requirements.txt`, `.gitignore`, README and GitHub Actions CI (system checks,
  missing-migration check, tests and deployment checks on Python 3.12 to 3.15).
