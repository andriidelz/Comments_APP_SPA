from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from .tasks import resize_image

@receiver(post_save, sender=Comment)
def handle_comment_save(sender, instance, created, **kwargs):
    if created and instance.image:
        resize_image.delay(instance.id)