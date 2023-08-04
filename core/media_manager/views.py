# media_uploader/views.py

import os
from django.conf import settings
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from core.mediaItems.models import MediaItem
from core.tasks import send_media_items_uploaded_email

class MediaUploaderView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        if "file" not in request.data or "path" not in request.data:
            return Response({"error": "File or path not provided"}, status=status.HTTP_400_BAD_REQUEST)

        media_item_id = request.data["public_id"]
        file = request.data["file"]
        path = request.data["path"]

        if ".." in os.path.abspath(path):
            return Response({"error": "Invalid upload path"}, status=status.HTTP_400_BAD_REQUEST)

        # Extract post ID and media item ID from the provided path
        post_id, file_name = os.path.split(path)

        # Ensure the upload path is inside the media folder
        upload_path = os.path.join(settings.MEDIA_ROOT, post_id)

        # Create the necessary directories if they don't exist
        os.makedirs(upload_path, exist_ok=True)

        # file_name = os.path.basename(file.name)
        file_path = os.path.join(upload_path, file_name)

        with open(file_path, "wb") as destination_file:
            for chunk in file.chunks():
                destination_file.write(chunk)

        try:
            media_item = MediaItem.objects.get_object_by_public_id(media_item_id)
            if media_item.state != 'UPLOADED':
                media_item.state = 'UPLOADED'
                media_item.save()

                # Check if all media items for the post are uploaded
                all_uploaded = media_item.post.media_items.filter(state='CREATED').count() == 0
                if all_uploaded:
                    # Trigger a Celery task to send the email
                    send_media_items_uploaded_email.delay(media_item.post_id)

        except MediaItem.DoesNotExist:
            return Response({"error": "MediaItem not found"}, status=status.HTTP_404_NOT_FOUND)



        return Response({"message": "File uploaded successfully"}, status=status.HTTP_200_OK)
