FROM node:20-bookworm-slim AS npm-builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts


FROM python:3.13-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    APP_BIND_ADDRESS=0.0.0.0 \
    APP_PORT=8000 \
    APP_WORKERS=4

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gettext \
    libffi8 \
    libharfbuzz-subset0 \
    libjpeg62-turbo \
    libopenjp2-7 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir poetry==2.3.3

COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --only main --no-root --no-interaction --no-ansi

RUN mkdir -p /app/static/npm_components
COPY --from=npm-builder /app/node_modules/ /app/static/npm_components/

COPY --chown=www-data:www-data elearning/ /app/elearning/
COPY --chown=www-data:www-data locale/ /app/locale/
COPY --chown=www-data:www-data scripts/ /app/scripts/
COPY --chown=www-data:www-data manage.py /app/manage.py
COPY --chown=www-data:www-data docker/config.py /app/elearning/config.py
COPY --chown=www-data:www-data docker/docker-init.sh /app/docker-init.sh

RUN chmod 755 /app/docker-init.sh \
    && mkdir -p /app/elearning/static /app/theme \
    && chown -R www-data:www-data /app

USER www-data

EXPOSE 8000

ENTRYPOINT ["/app/docker-init.sh"]
