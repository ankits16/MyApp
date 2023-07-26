from django.urls import path
from .views import MediaUploaderView

urlpatterns = [
    path('upload/', MediaUploaderView.as_view(), name='media_item_upload'),
]