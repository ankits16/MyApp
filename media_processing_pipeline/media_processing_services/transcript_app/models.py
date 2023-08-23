from django.db import models

# Create your models here.


class TranscriptionTask(models.Model):
    video_url = models.URLField()
    callback_url = models.URLField()
    celery_task_id = models.CharField(max_length=255, null=True, blank=True)  # New field
    status = models.CharField(
        max_length=10,
        choices=(
            ('PENDING', 'Pending'),
            ('PROCESSING', 'Processing'),
            ('DONE', 'Done'),
            ('ERROR', 'Error')
        ),
        default='PENDING'
    )
    result = models.TextField(null=True, blank=True)
