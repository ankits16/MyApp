from django.db import models
from core.abstract.models import AbstractManager, AbstractModel
# Create your models here.

class MediaItemManager(AbstractManager):
    pass

class MediaItem(AbstractModel):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('pdf', 'PDF'),
        # Add more choices as needed
    ]
    MEDIA_ITEM_STATES = [
        ('CREATED', 'Created'),
        ('UPLOADED', 'Uploaded'),
    ]
    post = models.ForeignKey(to='core_post.Post', on_delete=models.CASCADE, related_name="media_items")
    type = models.CharField(max_length=255, choices=MEDIA_TYPE_CHOICES)
    url = models.JSONField(blank=True, null=True)
    meta = models.JSONField(default=dict)
    state = models.CharField(max_length=20, choices=MEDIA_ITEM_STATES, default='CREATED')
    objects = MediaItemManager()

    def __str__(self) -> str:
        return f'{self.post.author.name}:{self.post.body}:{self.type}'
