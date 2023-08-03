# Generated by Django 4.0 on 2023-08-03 03:44

from django.db import migrations, models
from django.conf import settings
import os

def set_media_item_states(apps, schema_editor):
    MediaItem = apps.get_model('core_mediaItems', 'MediaItem')

    for media_item in MediaItem.objects.all():
        file_path = media_item.url.get('file_path')
        if file_path and os.path.exists(os.path.join(settings.MEDIA_ROOT, file_path)):
            media_item.state = 'UPLOADED'
        else:
            media_item.state = 'CREATED'
        media_item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core_mediaItems', '0005_alter_mediaitem_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediaitem',
            name='state',
            field=models.CharField(choices=[('CREATED', 'Created'), ('UPLOADED', 'Uploaded')], default='CREATED', max_length=20),
        ),
        migrations.RunPython(set_media_item_states),
    ]
