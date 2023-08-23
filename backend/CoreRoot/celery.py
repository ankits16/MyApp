from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CoreRoot.settings')
app = Celery('CoreRoot')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.CELERY_RESULT_BACKEND = 'django-db'
# Configure Celery to use RabbitMQ as the message broker
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = 'pyamqp://guest@localhost//'  # Use your RabbitMQ URL

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))