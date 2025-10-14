# Comments SPA Application

This is a test task for a comments system SPA.

## Features

- User can post comments with nesting (replies).
- Form: User Name, Email (required), Home page (optional), CAPTCHA, Text (with allowed HTML: a>, code>, i>, strong>).
- Upload image (JPG/GIF/PNG, resize to 320x240) or TXT file (<100KB).
- Pagination (25 per page), sorting by User Name, Email, Date (asc/desc, default LIFO desc).
- Real-time updates via WebSocket.
- Preview message without reload.
- Toolbar for HTML tags.
- Validation on client/server.
- Protection from XSS (bleach) and SQL injection (ORM).
- Async tasks (Celery for image resize).
- Cache (Redis for comment lists).
- Events (Django signals for post-save).
- JWT for API auth (token issued on post).

## Setup

1. Install Docker.
2. Run `docker-compose up --build`.
3. Backend at <http://localhost:8000/api/comments/>
4. Frontend at <http://localhost:5173/>
5. Migrate DB: `docker exec -it backend python manage.py migrate`
6. Create superuser: `docker exec -it backend python manage.py createsuperuser`
7. For CAPTCHA, run `docker exec -it backend python manage.py migrate captcha`

## Create Superuser

docker-compose exec backend python manage.py createsuperuser:

- username
- e-mail
- password

## Migrations

They are done automatically but there are few commands below anyway:

- docker-compose exec backend python manage.py migrate
- docker-compose exec backend python manage.py shell
- docker-compose exec backend python manage.py makemigrations

## Token

To get it:

- curl -X POST <http://localhost:8000/api/token/> \
     -H "Content-Type: application/json" \
     -d '{"username":"user","password":"qwerty123"}' - for example

## Getting and creating comments

- curl -X GET <http://localhost:8000/api/comments/> \
       -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

- curl -X POST <http://localhost:8000/api/comments/> \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello from curl!"}'

## DB Schema

Open db_schema.mwb in MySQL Workbench.

## Video

(Record a short video demoing the app.)

## Self-Check

Clone repo, follow setup—app should run from scratch.
