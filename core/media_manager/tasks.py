from celery import shared_task
from core.mediaItems.models import ProcessedMediaItemResult
from core.post.models import Post
from django.conf import settings

import requests
import json

def send_media_for_transcription(media_url, process_id):
    
    transcription_service_url = settings.TRANSCRIPTION_SERVICE_URL
    callback_url = settings.CALLBACK_URL
    print (f"Sending media for transcript at {transcription_service_url} calback = {callback_url}")
    # Construct payload for the transcription microservice

    # Construct payload for the transcription microservice
    payload = {
        "video_url": media_url,
        "callback_url": callback_url,
        "process_id": process_id  # Make sure to obtain this value when triggering the task
    }
    
    # # Convert Python dictionary to JSON string
    data = json.dumps(payload)
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Make an asynchronous request to the transcription service
    response = requests.post(transcription_service_url, data=data, headers=headers)
    
    
    # Make an asynchronous request to the transcription service
    # response = requests.post(transcription_service_url, body=data)
    if response.status_code != 200:
        # Log or handle the error as per your needs
        pass


@shared_task
def send_media_for_processing(post_id, request):
     try:
        print (f"Sending media {post_id}")
        post = Post.objects.get(pk=post_id)
        # "{{ scheme }}://{{ host }}{{root}}/{{ media_item.url.file_path }}"
        video_media_items = post.media_items.filter(type='video')
        for media_item in video_media_items:
            processing = ProcessedMediaItemResult.objects.create(media_item=media_item, service_name='test', output = {})
            processing.save()
            file_path =  media_item.url['file_path']
            if settings.DEBUG:
                host = 'host.docker.internal:8000'
            else:
                host = request.get("host")
            media_url = f'{ request.get("scheme") }://{host}/{settings.MEDIA_URL}{file_path}'
            print(f'**** media url is {media_url}')
            send_media_for_transcription(media_url, processing.public_id.hex)
     except Post.DoesNotExist:
        pass  # H

