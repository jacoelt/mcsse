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
| Frontend | React 18, Tailwind CSS, Vite |
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

\* These sites are behind Cloudflare JS challenges and are currently stubbed out. They need browser automation (e.g. Playwright) to scrape.

## Setup

### Prerequisites

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
```

### Environment variables (optional)

Set these for production or to use PostgreSQL locally:

```
DATABASE_URL=postgres://user:pass@host:port/dbname
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
CORS_ALLOWED_ORIGINS=https://your-frontend.com
FETCH_API_KEY=your-fetch-key
```

## Running locally

Start both servers:

```bash
# Terminal 1 — backend (runs on :8000)
cd back
source venv/Scripts/activate
python manage.py runserver

# Terminal 2 — frontend (runs on :5173, proxies /api to :8000)
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

### Scheduled fetching

Render's free tier doesn't support cron jobs. The API exposes a protected endpoint for external cron services (e.g. cron-job.org):

```
POST /api/internal/fetch/
Header: X-Fetch-Key: <your FETCH_API_KEY>
Query: mode=full (daily) or mode=players (hourly)
```

## Tests

The backend has 52 tests covering models, API endpoints, and the reconciler (deduplication/merge logic). Coverage is at 96%.

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

## Caveats

- **Cloudflare-protected sites**: 4 of the 9 sources are behind Cloudflare JS challenges and don't return data with plain HTTP requests. Implementing these requires a headless browser solution like Playwright.
- **Trigram search**: The name search uses PostgreSQL's `pg_trgm` extension for fuzzy matching. On SQLite (local dev), it falls back to `icontains` which is a simple substring match. Run `CREATE EXTENSION IF NOT EXISTS pg_trgm;` on your PostgreSQL database to enable it.
- **Rate limiting**: The fetchers don't currently implement rate limiting or request delays between pages. If a source starts blocking requests, add delays in the fetcher's page loop.
- **Render free tier spin-down**: The free web service spins down after 15 minutes of inactivity. The first request after spin-down takes ~30 seconds.
