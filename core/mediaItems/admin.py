from django.contrib import admin
from .models import MediaItem

# Register your models here.
@admin.register(MediaItem)
class MediItemAdmin(admin.ModelAdmin):
    list_display = ['post', 'type', 'meta' ]