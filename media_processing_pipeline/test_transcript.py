import subprocess

import numpy as np
import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
import io

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/Users/ankit/Downloads/testspeech-396803-f70166f75e44.json'


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


def transcribe_audio(audio_path, model_path):
    client = speech.SpeechClient()

    with io.open(audio_path, 'rb') as audio_file:
        content = audio_file.read()

    # audio = types.RecognitionAudio(content=content)
    # config = types.RecognitionConfig(
    #     encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    #     sample_rate_hertz=16000,
    #     language_code="en-US",  # Primary language set to English
    # )

    # response = client.recognize(config=config, audio=audio)

    # for result in response.results:
    #     return result.alternatives[0].transcript
    return "Dummy transcript"


def main():
    video_path = '/Users/ankit/Documents/code/web learnings/django/myapp/backend/uploaded_media_items/d6d3c09b522c47bba882b6133af78643/0081f24c17cc496db15c2e0b80502128.mp4'
    temporary_audio_path = os.path.join(os.getcwd(), 'temp_audio.wav')
    deepspeech_model_path = '/Users/ankit/Documents/code/web learnings/django/myapp/media_processing_pipeline/media_processing_services/assets/model/deepspeech-0.9.3-models.pbmm'
    print(os.getcwd())
    if os.path.isfile(video_path):
        print(f"The file {video_path} exists.")
        extract_audio_from_video(video_path, temporary_audio_path)
        transcript = transcribe_audio(
            temporary_audio_path, deepspeech_model_path)
        print(transcript)
    else:
        print(f"The file {video_path} does not exist.")


if __name__ == "__main__":
    main()
