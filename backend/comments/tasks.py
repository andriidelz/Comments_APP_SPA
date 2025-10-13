from celery import shared_task
from .models import Comment
from PIL import Image
from django.core.files.base import ContentFile
import io

@shared_task
def resize_image(comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.image:
        img = Image.open(comment.image.path)
        if img.width > 320 or img.height > 240:
            img.thumbnail((320, 240))
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG')
            comment.image.save(comment.image.name, ContentFile(buffer.getvalue()), save=False)
        comment.save()