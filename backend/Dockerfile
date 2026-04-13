FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    postgresql-client \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install setuptools && \
    pip install -r requirements.txt && \
    printf 'from importlib.metadata import version, PackageNotFoundError\ntry:\n    __version__ = version("djangorestframework-simplejwt")\nexcept PackageNotFoundError:\n    __version__ = "unknown"\n' \
        > /usr/local/lib/python3.12/site-packages/rest_framework_simplejwt/__init__.py

COPY . .

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["daphne", "-b", "0.0.0.0", "-p", "10000", "comments_app.asgi:application"]