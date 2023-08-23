# media_uploader/views.py

import os
from django.conf import settings
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from core.mediaItems.models import MediaItem, ProcessedMediaItemResult
from core.tasks import send_media_items_uploaded_email
from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg import openapi
from .tasks import send_media_for_processing

class MediaUploaderView(APIView):
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        operation_description="Upload a media file and associate it with a post.",
        # request_body=MySerializer,  # Replace with your request serializer class
        manual_parameters=[
            openapi.Parameter(
                name="public_id",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="The public ID for the media item.",
                required=True,
                example="abcd1234",
            ),
            openapi.Parameter(
                name="file",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="The media file to upload.",
                required=True,
            ),
            openapi.Parameter(
                name="path",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="The path to save the media file.",
                required=True,
                example="32d4f073f77148f9afe72f23aaca2905/myfile.jpg",
            ),
        ],
        responses={
            status.HTTP_200_OK: "Successful response",
            status.HTTP_400_BAD_REQUEST: "Bad request",
        }
    )
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
            media_item = MediaItem.objects.get_object_by_public_id(
                media_item_id)
            media_item.state = ''
            if media_item.state != 'UPLOADED':
                media_item.state = 'UPLOADED'
                media_item.save()
                
                # Check if all media items for the post are uploaded
                all_uploaded = media_item.post.media_items.filter(
                    state='CREATED').count() == 0
                if all_uploaded:
                    # Trigger a Celery task to send the email
                    request_data = {
                        "scheme": request.scheme,
                        "host": request.get_host(),
                    }
                    # send_media_items_uploaded_email.delay(
                    #     media_item.post_id, request_data)
                    send_media_for_processing.delay(media_item.post_id, request_data)

        except MediaItem.DoesNotExist:
            return Response({"error": "MediaItem not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "File uploaded successfully"}, status=status.HTTP_200_OK)
