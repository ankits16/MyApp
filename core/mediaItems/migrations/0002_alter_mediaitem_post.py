# Generated by Django 4.0 on 2023-07-13 01:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_post', '0001_initial'),
        ('core_mediaItems', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaitem',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media_items', to='core_post.post'),
        ),
    ]
