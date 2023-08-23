
import os
import uuid
import requests
import subprocess

from celery import shared_task

from django.conf import settings
from datetime import datetime

from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types

from .models import TranscriptionTask

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS

def get_unique_filename(extension):
    """Generates a unique filename using a UUID."""
    return f"{uuid.uuid4()}.{extension}"


@shared_task(queue='transcription')
def transcribe_task(task_id):
    print(f'start processing task {task_id}')
    task = TranscriptionTask.objects.get(pk=task_id)
    task.status = "PROCESSING"
    task.save()

    video_path = get_unique_filename('mp4')
    audio_path = get_unique_filename('wav')
    
    try:
        # Download video
        response = requests.get(task.video_url, stream=True)
        with open(video_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Extract audio and transcribe
        extract_audio_from_video(video_path, audio_path)
        transcript = transcribe_audio(audio_path)
        task.result = transcript
        task.status = "DONE"
        
        # Send results to callback URL
        requests.post(task.callback_url, json={"transcript": transcript, "task_id": task_id})
    except Exception as e:
        task.status = "ERROR"
        task.result = str(e)
        
    task.save()
    os.remove(video_path)
    os.remove(audio_path)

def extract_audio_from_video(video_path, output_audio_path):
    command = [
        'ffmpeg',
        '-y',                   # Overwrite output files without asking.
        '-i', video_path,
        '-ac', '1',             # Set audio channels to mono.
        '-ar', '16000',         # Set audio rate to 16kHz.
        '-q:a', '0',            # Quality setting, 0 means highest quality.
        '-map', 'a',
        output_audio_path
    ]
    subprocess.run(command, check=True)

def transcribe_audio(audio_path):
    client = speech.SpeechClient()

    with open(audio_path, 'rb') as audio_file:
        content = audio_file.read()

    # audio = speech.RecognitionAudio(content=content)
    # config = types.RecognitionConfig(
    #     encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    #     sample_rate_hertz=16000,
    #     language_code="en-US",  # Primary language set to English
    # )

    # response = client.recognize(config=config, audio=audio)
    # return ''.join([result.alternatives[0].transcript for result in response.results])
    return f"Dummy transcript {datetime.now()}"