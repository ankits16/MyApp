import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'media_processing_services.settings')

app = Celery('media_processing_services')
app.conf.broker_url = 'pyamqp://guest@localhost//'  # Use your RabbitMQ URL
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)