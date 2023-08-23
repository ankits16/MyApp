
from core.abstract.viewsets import AbstractViewSet
from .models import MediaItem, ProcessedMediaItemResult
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import MediaItemSerializer
from rest_framework.exceptions import NotFound


class MediaItemViewSet(viewsets.ModelViewSet):
    queryset = MediaItem.objects.all()
    serializer_class = MediaItemSerializer


class ProcessedMediaItemCallbackViewSet(AbstractViewSet):

    def create(self, request, *args, **kwargs):
        processing_id = request.data.get('process_id')
        inference = ProcessedMediaItemResult.objects.get_object_by_public_id(
            processing_id)
        if not inference:
            raise NotFound(detail="ProcessedMediaItemResult not found")
        inference.service_name = request.data.get('service_name')
        inference.output = request.data.get('result')
        inference.save()

        return Response({"status": "Received and saved transcript"}, status=status.HTTP_201_CREATED)
