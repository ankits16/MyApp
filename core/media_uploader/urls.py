from django.urls import path
from .views import MediaUploaderView

urlpatterns = [
    path('', MediaUploaderView.as_view(), name='media_item_upload'),
]