# Backend image for the MC Server Search Engine.
#
# Runs gunicorn by default (production shape). docker-compose.yml overrides the
# command with `manage.py runserver` for local development.
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependencies are installed before the source is copied so that editing code
# does not invalidate the (slow) pip layer.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run as a non-root user. Ownership of /app matters for collectstatic, which
# writes into staticfiles/.
RUN useradd --create-home --uid 10001 app \
 && mkdir -p /app/staticfiles \
 && chown -R app:app /app
USER app

EXPOSE 8000

CMD ["gunicorn", "main.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--access-logfile", "-"]
