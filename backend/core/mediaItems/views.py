import os

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import MediaItem, ProcessedMediaItemResult

from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MediaItemSerializer

class MediaItemUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, post_id):
        return Response({"message": "Media item uploaded successfully"}, status=status.HTTP_200_OK)