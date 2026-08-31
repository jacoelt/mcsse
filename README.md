# MC Server Search Engine

A search engine for Minecraft servers that aggregates data from multiple listing sites and lets users filter by objective criteria — not just votes and popularity.

## Features

- **Multi-source aggregation**: Fetches server data from 9 listing sites, deduplicates by IP:port, and reconciles fields using a source priority system
- **Search & filter**: Server name, game version, edition (Java/Bedrock/both), online players, max players, votes, country, tags — all with range filters using exponential buckets
- **Server detail pages**: Full description, tags, IP with copy button, links, and source listings
- **Auto-generated tags**: Tags are collected and merged from all sources automatically
- **Infinite scroll**: Results load continuously as you scroll
- **Shareable searches**: All filter state is synced to URL query params

## Tech stack

| Layer | Tech |
|-------|------|
| Backend | Python 3.13, Django 6, Django-Ninja |
| Frontend | React 19, Tailwind CSS 4, Vite |
| Database | PostgreSQL (SQLite for local dev) |
| Hosting | Render.com (free tier) + Aiven PostgreSQL |

## Data sources

Servers are fetched from these listing sites (priority order, highest first):

1. minecraft-mp.com
2. minecraftservers.org
3. minecraft-server-list.com *
4. planetminecraft.com *
5. best-minecraft-servers.co
6. findmcserver.com *
7. topg.org
8. minecraft.buzz
9. serveur-minecraft.com *

\* These sites sit behind Cloudflare. They are scraped via [`curl_cffi`](https://github.com/lexiforest/curl_cffi) browser TLS impersonation rather than plain HTTP — no headless browser required. `findmcserver.com` is read from its JSON API; the other three are HTML-scraped.

## Setup

### Prerequisites

Either Docker (see [Running with Docker](#running-with-docker) — nothing else needed), or a local toolchain:

- Python 3.13+
- Node.js 18+
- PostgreSQL (optional — SQLite works for local dev)

### Backend

```bash
cd back
python -m venv venv

# Windows
source venv/Scripts/activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # optional, for admin access
```

### Frontend

```bash
cd front
npm install
cp .env.dist .env  # dev defaults point the UI at http://localhost:8000
```

### Environment variables

Both `back/` and `front/` follow the same pattern: copy `.env.dist` to `.env` (gitignored) and edit the values.

**Backend** (`back/.env`) — set these for production or to use PostgreSQL locally:

```
DATABASE_URL=postgres://user:pass@host:port/dbname
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
CORS_ALLOWED_ORIGINS=https://your-frontend.com
FETCH_API_KEY=your-fetch-key
```

**Frontend** (`front/.env`):

```
VITE_API_HOST=http://localhost:8000   # base URL of the backend API, no trailing slash
```

## Running with Docker

The fastest path, and the only one that works on a host where policy blocks unsigned
Python builds (e.g. Windows with Smart App Control enabled). Requires nothing but Docker.

```bash
docker compose up
```

That starts three services:

| Service | Port | Notes |
|---------|------|-------|
| `db` | 5432 | `postgres:17-alpine`, data persisted in the `pgdata` volume |
| `api` | 8000 | Migrates on boot, then `runserver` with live reload |
| `front` | 5173 | `npm install` + `vite dev`, live reload |

Then open http://localhost:5173.

Postgres is the default so `pg_trgm` and the trigram GIN index are actually exercised,
matching production. To use SQLite instead:

```bash
DATABASE_URL=sqlite:///db.sqlite3 docker compose up api
```

`back/` and `front/` are bind-mounted, so edits on the host reload without a rebuild.
Rebuild only when `requirements.txt` changes:

```bash
docker compose build api
```

Run any management command in the container:

```bash
docker compose run --rm api python manage.py migrate
docker compose run --rm api python manage.py fetch_servers --source=minecraft-mp
docker compose run --rm api python manage.py createsuperuser
```

Set `SUPER_USER_USERNAME` and `SUPER_USER_PASSWORD` in the environment and migration
`core.0002` creates an admin user for you on first boot.

## Running locally

Without Docker. Start both servers:

```bash
# Terminal 1 — backend (runs on :8000)
cd back
source venv/Scripts/activate
python manage.py runserver

# Terminal 2 — frontend (runs on :5173, talks to the API at $VITE_API_HOST)
cd front
npm run dev
```

Open http://localhost:5173

### Fetching server data

Full fetch (daily — pulls all server data from all sources):

```bash
cd back
source venv/Scripts/activate
python manage.py fetch_servers
```

Fetch from a single source:

```bash
python manage.py fetch_servers --source=minecraft-mp
```

Player count update only (hourly):

```bash
python manage.py update_players
```

### Admin

Django admin is available at http://localhost:8000/admin/ (requires a superuser).

## Deployment

The project includes a `render.yaml` for one-click deployment on Render.com:

- **mcsse-api**: Django web service (free tier)
- **mcsse-front**: Static site serving the React build (free tier)

The database should be provisioned separately on Aiven (free tier) and the `DATABASE_URL` env var set on the API service.

> **`render.yaml` is known to be drifted.** It has not been modified since the initial commit, yet `uvicorn` was later added to `requirements.txt` for a `gunicorn` `UvicornWorker` — a worker class the committed `startCommand` does not use. The live start command was changed in the Render dashboard rather than here. Treat this file as a starting point, not as a record of the deployed configuration, and reconcile it against the dashboard before redeploying.

### Scheduled fetching

Render's free tier doesn't support cron jobs. The API exposes a protected endpoint for external cron services (e.g. cron-job.org):

```
POST /api/internal/fetch/
Header: X-Fetch-Key: <your FETCH_API_KEY>
Query: mode=full (daily) or mode=players (hourly)
```

## Tests

The backend has 103 tests covering models, API endpoints, the reconciler (deduplication/merge logic), tag normalization, and two of the scrapers. The coverage gate is configured in `setup.cfg` at `fail_under = 80`.

In Docker (no local Python needed):

```bash
docker compose run --rm api python manage.py test core.tests fetcher.tests
```

Or against a local venv:

```bash
cd back
source venv/Scripts/activate  # or source venv/bin/activate on Linux/macOS

# Run all tests
python manage.py test core.tests fetcher.tests

# Run with verbose output
python manage.py test core.tests fetcher.tests -v 2

# Run with coverage
coverage run manage.py test core.tests fetcher.tests
coverage report

# HTML coverage report
coverage html
# then open htmlcov/index.html
```

### What's tested

- **Models** (`core/tests/test_models.py`): CRUD, relationships, unique constraints, default ordering, cascade deletes
- **API** (`core/tests/test_api.py`): All search filters (name, version, edition, player range, vote range, country, tags, combined), sorting, pagination, clamping, server detail with tags/sources, filters endpoint with counts
- **Reconciler** (`fetcher/tests/test_reconciler.py`): Dedup by IP:port, dedup by name fallback, source priority for field selection, vote summing, tag union, longest description, empty-field fallthrough, source tracking, player count updates
- **Tag rules** (`fetcher/tests/test_tag_rules.py`): Canonical normalization — case/whitespace, separator collapse, unicode stripping, safe singularization, stopword and bare-numeric drops, alias rewriting (single-step, non-transitive), display-name fallback
- **Tag reconcile command** (`fetcher/tests/test_reconcile_tags_command.py`): Rename-in-place vs merge-into-canonical, m2m dedup on merge, deletion of stopword/numeric tags, `--dry-run`, idempotency on clean data
- **Scraper edge cases** (`fetcher/tests/test_findmcserver.py`, `test_planetminecraft.py`): Country codes restricted to ISO 3166-1 alpha-2, and rejection of sentinel/inflated player counts

## Caveats

- **Cloudflare-protected sites**: 4 of the 9 sources sit behind Cloudflare and return a challenge to plain HTTP requests. They are handled with `curl_cffi` TLS impersonation. If a site tightens its protection, that fetcher is the first thing to break — check it before assuming the parser is at fault.
- **Trigram search**: The name search uses PostgreSQL's `pg_trgm` extension for fuzzy matching. On SQLite (local dev), it falls back to `icontains` which is a simple substring match. Run `CREATE EXTENSION IF NOT EXISTS pg_trgm;` on your PostgreSQL database to enable it.
- **Rate limiting**: The fetchers don't currently implement rate limiting or request delays between pages. If a source starts blocking requests, add delays in the fetcher's page loop.
- **Render free tier spin-down**: The free web service spins down after 15 minutes of inactivity. The first request after spin-down takes ~30 seconds.
