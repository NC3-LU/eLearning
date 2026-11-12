# Run Alto with Docker

The Docker layout follows Governance Platform's separation between the Django
application, PostgreSQL, and the independently versioned theme.

## Start

From the Alto repository root:

```bash
docker compose -f docker/docker-compose.yml up --build -d
docker compose -f docker/docker-compose.yml ps
```

The application is available at <http://127.0.0.1:8000> by default.

The development defaults match `elearning/config_dev.py`. Set at least
`POSTGRES_PASSWORD`, `SECRET_KEY`, and `HASH_KEY` to new secret values before
using this stack outside local development. Other supported variables include
`POSTGRES_DB`, `POSTGRES_USER`, `APP_BIND_ADDRESS`, `APP_PORT`, `ALLOWED_HOSTS`,
`PUBLIC_URL`, and `APP_WORKERS`.

## Load course data

After the first startup, load the fixture from the theme image:

```bash
docker compose -f docker/docker-compose.yml exec web ./scripts/load_data.sh
```

## Theme updates

The `theme` service builds `theme/docker/Dockerfile` and initializes the
`theme_data` volume. Docker only copies image content into a new volume. To
apply a newly built theme, recreate only that volume:

```bash
docker compose -f docker/docker-compose.yml down
docker volume rm alto_theme_data
docker compose -f docker/docker-compose.yml up --build -d
```

Do not use `docker compose down -v` on an installation containing data: that
also removes the PostgreSQL volume.

## PostgreSQL 18

The database image is pinned to PostgreSQL 18.6. PostgreSQL 18 stores its data
under `/var/lib/postgresql`, which is mounted as the `postgres_data` volume.
An existing PostgreSQL 16 data directory cannot be mounted directly into this
container; migrate it with `pg_dump`/`pg_restore` or `pg_upgrade`.
