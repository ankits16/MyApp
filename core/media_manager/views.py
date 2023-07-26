# media_uploader/views.py

import os
from django.conf import settings
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

class MediaUploaderView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        if "file" not in request.data or "path" not in request.data:
            return Response({"error": "File or path not provided"}, status=status.HTTP_400_BAD_REQUEST)

        file = request.data["file"]
        upload_path = request.data["path"]

        if ".." in os.path.abspath(upload_path):
            return Response({"error": "Invalid upload path"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the upload path is inside the media folder
        upload_path = os.path.join(settings.MEDIA_ROOT, upload_path)

        # Create the necessary directories if they don't exist
        os.makedirs(upload_path, exist_ok=True)

        file_name = file.name
        file_path = os.path.join(upload_path, file_name)

        with open(file_path, "wb") as destination_file:
            for chunk in file.chunks():
                destination_file.write(chunk)

        return Response({"message": "File uploaded successfully"}, status=status.HTTP_200_OK)
