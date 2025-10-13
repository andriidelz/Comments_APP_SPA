from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import bleach
from django.conf import settings

ALLOWED_TAGS = ['a', 'code', 'i', 'strong']
ALLOWED_ATTRIBUTES = {'a': ['href', 'title']}

class Comment(MPTTModel):
    user_name = models.CharField(max_length=255)
    email = models.EmailField()
    home_page = models.URLField(blank=True, null=True)
    text = models.TextField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['created_at']

    def save(self, *args, **kwargs):
        self.text = bleach.clean(self.text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user_name} - {self.created_at}'