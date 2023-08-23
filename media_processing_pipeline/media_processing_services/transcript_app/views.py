import requests
import os
import subprocess
import json
import uuid



from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


from .models import TranscriptionTask
from .tasks import transcribe_task


@method_decorator(csrf_exempt, name='dispatch')
class TranscribeView(View):
    
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            video_url = data.get('video_url')
            callback_url = data.get('callback_url')
            process_id = data.get('process_id')

            if not video_url or not callback_url:
                return JsonResponse({"error": "Both 'video_url' and 'callback_url' are required."}, status=400)

            task = TranscriptionTask(video_url=video_url, callback_url=callback_url)
            task.save()

            # Schedule the transcription task
            print(f'calling transcribe_task  {task.id}')
            result = transcribe_task.delay(task.id, process_id)
            
            # # Save the Celery task ID to your model
            task.celery_task_id = result.id
            task.save()
            print(f'scheduled with task  {result.id}')
            
            return JsonResponse({"status": "Task scheduled", "task_id": task.id, "celery_id": result.id}, status=202)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    


