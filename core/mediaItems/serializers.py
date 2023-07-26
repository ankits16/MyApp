from django.conf import settings
from rest_framework import serializers
from .models import MediaItem
from core.post.models import Post
from core.abstract.serializers import AbstractSerializer



class MediaItemSerializer(AbstractSerializer):
    
    '''returns the uuid of the parent post 
    we dont want to send the pk or the id (which is usually an incremental value)
    '''
    post = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='public_id')
    parent_post_id = serializers.UUIDField(source='post.public_id', read_only=True, format='hex')
    url = serializers.SerializerMethodField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        post = Post.objects.get_object_by_public_id(representation['post'])
        representation['post'] = post.public_id.hex  # Convert post to string format
        return representation
    
    def get_url(self, obj):
        request = self.context.get('request')
        if request and request.method == 'GET':
            # Assuming 'MEDIA_URL' setting is properly configured
            return f"{settings.MEDIA_URL}{obj.url['file_path']}"
        else:
            return obj.url
    
    class Meta:
        model = MediaItem
        fields = ['id', 'type', 'meta', 'url', 'post', 'parent_post_id', 'created', 'updated']
        extra_kwargs = {
            'url': {'required': False},
            'post': {'required': False}
        }

    