from django.contrib import admin
from .models import MediaItem

from django_celery_results.models import TaskResult
from django_celery_results.admin import TaskResultAdmin as BaseTaskResultAdmin

class CustomTaskResultAdmin(BaseTaskResultAdmin):
    list_display = ('task_id', 'status', 'date_done')  # Customize as needed

# Register the customized admin class
admin.site.unregister(TaskResult)
admin.site.register(TaskResult, CustomTaskResultAdmin)
# # Register your models here.
@admin.register(MediaItem)
class MediItemAdmin(admin.ModelAdmin):
    list_display = ['post', 'type', 'meta' ]