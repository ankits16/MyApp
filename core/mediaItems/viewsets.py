from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import MediaItem
from .serializers import MediaItemSerializer

class MediaItemViewSet(viewsets.ModelViewSet):
    queryset = MediaItem.objects.all()
    serializer_class = MediaItemSerializer