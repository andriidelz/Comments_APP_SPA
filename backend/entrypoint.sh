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

  echo "🧑‍💼 Creating default user (user / supersecret) if not exists..."
    python manage.py shell << EOF
from django.contrib.auth.models import User

if not User.objects.filter(username='user').exists():
    User.objects.create_user(
        username='user',
        password='supersecret',
        is_active=True,
        is_staff=True
    )
    print('✅ Default user "user" created successfully!')
else:
    print('ℹ️  User "user" already exists')
EOF

  echo "🧹 Collecting static files..."
  python manage.py collectstatic --noinput
fi

echo "🚀 Starting ASGI server with Daphne..."
exec daphne \
  --bind 0.0.0.0 \
  --port ${PORT:-8000} \
  comments_app.asgi:application

exec "$@"

# echo "🚀 Starting Django server..."
# exec python manage.py runserver 0.0.0.0:8000
