from django.urls import path
from .views import TranscribeView

urlpatterns = [
    path('transcripts/', TranscribeView.as_view(), name='transcripts'),
]