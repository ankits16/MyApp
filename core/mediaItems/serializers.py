from rest_framework import serializers
from .models import MediaItem
from core.post.models import Post
from core.abstract.serializers import AbstractSerializer



class MediaItemSerializer(AbstractSerializer):
    
    '''returns the uuid of the parent post 
    we dont want to send the pk or the id (which is usually an incremental value)
    '''
    parent_post_id = serializers.UUIDField(source='post.public_id', read_only=True, format='hex')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['post'] = str(representation['post'])  # Convert post to string format
        return representation
    
    class Meta:
        model = MediaItem
        fields = ['id', 'type', 'meta', 'url', 'post', 'parent_post_id', 'created', 'updated']
        extra_kwargs = {
            'url': {'required': False},
            'post': {'required': False}
        }

    