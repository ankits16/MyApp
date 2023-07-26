import os
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from core.abstract.viewsets import AbstractViewSet
from core.post.models import Post
from core.mediaItems.serializers import MediaItemSerializer
from core.post.serializers import PostSerializer
from core.auth.permissions import UserPermission
from .url_factory import LocalMediaURLFactory

class PostViewSet(AbstractViewSet):
    http_method_names = ('post', 'get', 'put', 'delete')
    permission_classes = (UserPermission,)
    serializer_class = PostSerializer


    def get_queryset(self):
        return Post.objects.all()
    
    def get_object(self):
        obj = Post.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    
    def create(self, request, *args, **kwargs):
        post_data = request.data.copy()
        media_items_data = post_data.pop('media_items', [])

        post_serializer = self.get_serializer(data=post_data)
        post_serializer.is_valid(raise_exception=True)
        post = post_serializer.save()

        url_factory = LocalMediaURLFactory()
        media_items = []
        for media_item_data in media_items_data:
            file_name = media_item_data.pop('file_name')
            
            # Associate the Post with the MediaItem and set the URL
            media_item_data['post'] = post.public_id
            # media_item_data['url'] = url

            media_item_serializer = MediaItemSerializer(data=media_item_data)
            media_item_serializer.is_valid(raise_exception=True)
            media_item = media_item_serializer.save()

             # Generate the URL based on the provided file name
            file_extension = os.path.splitext(file_name)[1]
            file_path = url_factory.generate_url(post.public_id.hex, media_item.public_id.hex, file_extension)

            # Set the dynamically generated URL for the media item
            media_item.url = {'file_path' : file_path} 
            media_item.save()

            media_items.append(media_item)


        return Response(
            {
                'post': post_serializer.data,
                'media_items': MediaItemSerializer(media_items, many=True).data
            },
            status=status.HTTP_201_CREATED
        )
    
    # When detail=True
    #  the action will be accessible at a URL like /books/{id}/custom_action/
    #  when detail=False
    # the action will be accessible at a URL like /books/custom_action/.
    # action is a decorator
    # In Python, a decorator is a special type of function that can modify or enhance the behavior of another function or class
    @action(methods=['post'], detail=True)
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user
        user.like(post)
        serializer = self.serializer_class(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=True)
    def remove_like(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user
        user.remove_like(post)
        serializer = self.serializer_class(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

