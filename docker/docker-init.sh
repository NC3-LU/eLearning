#!/bin/bash

set -euo pipefail

if [ "$#" -gt 0 ]; then
    exec "$@"
fi

python manage.py migrate
python manage.py compilemessages
python manage.py collectstatic --clear --noinput

exec gunicorn elearning.wsgi \
    --workers "${APP_WORKERS:-4}" \
    --bind "${APP_BIND_ADDRESS:-0.0.0.0}:${APP_PORT:-8000}"
