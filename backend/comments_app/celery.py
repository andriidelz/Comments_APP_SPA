import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comments_app.settings')

app = Celery('comments_app')
app.config_from_object({
    'broker_url': os.getenv('REDIS_URL', 'redis://redis:6379/0'),
    'result_backend': os.getenv('REDIS_URL', 'redis://redis:6379/0'),
})

app.autodiscover_tasks()