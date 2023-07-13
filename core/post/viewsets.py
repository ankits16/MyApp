from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from core.abstract.viewsets import AbstractViewSet
from core.post.models import Post
from core.mediaItems.serializers import MediaItemSerializer
from core.post.serializers import PostSerializer
from core.auth.permissions import UserPermission

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
    
    def generate_media_item_url(self):
        return 'https://google.co.in'
    
    def create(self, request, *args, **kwargs):
        post_data = request.data.copy()
        media_items_data = post_data.pop('media_items', [])

        post_serializer = self.get_serializer(data=post_data)
        post_serializer.is_valid(raise_exception=True)
        post = post_serializer.save()

        media_items = []
        for media_item_data in media_items_data:
            # Generate the URL dynamically for each media item
            url = self.generate_media_item_url()

            # Associate the Post with the MediaItem and set the URL
            media_item_data['post'] = post.id
            media_item_data['url'] = url

            media_item_serializer = MediaItemSerializer(data=media_item_data)
            media_item_serializer.is_valid(raise_exception=True)
            media_item = media_item_serializer.save()

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

