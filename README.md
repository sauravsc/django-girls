# django-girls

[![CI](https://github.com/saurvs/django-girls/actions/workflows/ci.yml/badge.svg)](https://github.com/saurvs/django-girls/actions/workflows/ci.yml)

A small blog app built while following the [Django Girls Tutorial](https://tutorial.djangogirls.org/)
in 2018, updated to run on **Django 6.1** and **Python 3.12+** (CI tests 3.12 to 3.15).

It has a `Post` model (managed through the Django admin) and a post list page at `/` that renders
the tutorial's static `blog/post_list.html` template.

## Run it locally

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver         # serves http://127.0.0.1:8000/
```

With no environment variables set, the app runs in development mode: `DEBUG` is on, an
insecure development-only secret key is used, and only `127.0.0.1` and `localhost` are accepted
as hosts.

## Tests and checks

```sh
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

## Configuration

Settings that differ between development and production come from environment variables:

| Variable | Default | Meaning |
|---|---|---|
| `DJANGO_DEBUG` | `1` | Set to `0` in production. |
| `DJANGO_SECRET_KEY` | development-only key | Required when `DJANGO_DEBUG=0`; the app refuses to start without it. |
| `DJANGO_ALLOWED_HOSTS` | `127.0.0.1,localhost` | Comma-separated host names, e.g. `yourname.pythonanywhere.com`. |
| `DJANGO_HTTPS` | `0` | Set to `1` when the site is served over HTTPS: redirects HTTP to HTTPS, marks cookies `Secure` and sends HSTS. |
| `DJANGO_HSTS_SECONDS` | `3600` | HSTS max-age, used when `DJANGO_HTTPS=1`. |
| `DJANGO_HSTS_INCLUDE_SUBDOMAINS` | `0` | Adds `includeSubDomains` to HSTS. |
| `DJANGO_HSTS_PRELOAD` | `0` | Adds `preload` to HSTS. |
| `DJANGO_TRUST_X_FORWARDED_PROTO` | `0` | Trust `X-Forwarded-Proto: https` from a TLS-terminating proxy. Only enable it if the proxy sets that header itself. |

Generate a secret key with:

```sh
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Then check a production configuration with:

```sh
DJANGO_DEBUG=0 DJANGO_SECRET_KEY=... DJANGO_ALLOWED_HOSTS=example.com DJANGO_HTTPS=1 \
  python manage.py check --deploy
```

For static files in production, run `python manage.py collectstatic` (files go to `static/`).
