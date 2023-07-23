from django.contrib import admin
from .models import Post
from core.mediaItems.models import MediaItem


class MediaItemInline(admin.TabularInline):
    model = MediaItem
    classes = ['collapse']
   
    def get_extra(self, request, obj=None, **kwargs):
        # Set the number of extra forms to display (0 to hide the empty forms)
        return 0



# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'body', 'edited', ]
    inlines = [MediaItemInline]
    