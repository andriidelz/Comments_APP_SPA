#!/bin/sh
set -e

echo "📡 Waiting for PostgreSQL..."
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" > /dev/null 2>&1; do
  sleep 1
done

echo "✅ PostgreSQL is ready."

if [ "$RUN_MAIN" = "true" ]; then
  echo "⚙️ Running migrations (only once)..."
  python manage.py makemigrations --noinput
  python manage.py migrate --noinput

  echo "🧹 Collecting static files..."
  python manage.py collectstatic --noinput
fi

exec "$@"

# echo "🚀 Starting Django server..."
# exec python manage.py runserver 0.0.0.0:8000
