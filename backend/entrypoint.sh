#!/bin/sh
set -e

if [ -n "$POSTGRES_HOST" ]; then
  echo "📡 Waiting for PostgreSQL..."
  until pg_isready -h "$POSTGRES_HOST" -p "${POSTGRES_PORT:-5432}" -U "$POSTGRES_USER" > /dev/null 2>&1; do
    sleep 1
  done
  echo "✅ PostgreSQL is ready."
fi

if [ "$RUN_MAIN" = "true" ]; then
  echo "⚙️ Running migrations..."
  python manage.py migrate --noinput
  echo "🧹 Collecting static files..."
  python manage.py collectstatic --noinput
fi

exec "$@"

# echo "🚀 Starting Django server..."
# exec python manage.py runserver 0.0.0.0:8000
