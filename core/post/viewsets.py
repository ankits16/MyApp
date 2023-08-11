import os
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from core.abstract.viewsets import AbstractViewSet
from core.post.models import Post
from core.mediaItems.models import MediaItem
from core.mediaItems.serializers import MediaItemSerializer
from core.post.serializers import PostSerializer
from core.auth.permissions import UserPermission
from django.db.models import OuterRef, Subquery, Count, F, IntegerField
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class PostViewSet(AbstractViewSet):
    http_method_names = ('post', 'get', 'put', 'delete')
    permission_classes = (UserPermission,)
    serializer_class = PostSerializer

    def get_queryset(self):
        subquery = MediaItem.objects.filter(
            post_id=OuterRef('pk'),
            state='UPLOADED'
        ).values('post_id').annotate(uploaded_count=Count('pk')).values('uploaded_count')

        return Post.objects.annotate(
            total_media_count=Subquery(subquery)
        ).filter(total_media_count=Subquery(subquery, output_field=IntegerField()))

    def get_object(self):
        obj = Post.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    @swagger_auto_schema(
        operation_description="Create a new post with media items",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'author': openapi.Schema(type=openapi.TYPE_STRING),
                'body': openapi.Schema(type=openapi.TYPE_STRING),
                'media_items': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'type': openapi.Schema(type=openapi.TYPE_STRING),
                            'file_name': openapi.Schema(type=openapi.TYPE_STRING),
                            'meta': openapi.Schema(type=openapi.TYPE_OBJECT, additional_properties=True),
                        },
                    ),
                ),
            },
            required=['author', 'body', 'media_items'],
        ),
        responses={
            status.HTTP_201_CREATED: "Successful creation",
            status.HTTP_400_BAD_REQUEST: "Bad request",
        }
    )
    def create(self, request, *args, **kwargs):
        post_data = request.data.copy()
        media_items_data = post_data.pop('media_items', [])

        post_serializer = self.get_serializer(data=post_data)
        post_serializer.is_valid(raise_exception=True)
        post = post_serializer.save()

        media_items = []
        for media_item_data in media_items_data:
            file_name = media_item_data.pop('file_name')

            # Associate the Post with the MediaItem and set the URL
            media_item_data['post'] = post.public_id
            # media_item_data['url'] = url

            media_item_serializer = MediaItemSerializer(
                data=media_item_data, context=self.get_serializer_context())
            media_item_serializer.is_valid(raise_exception=True)
            media_item = media_item_serializer.save()

            # Generate the URL based on the provided file name
            file_extension = os.path.splitext(file_name)[1]

            # Set the dynamically generated URL for the media item
            media_item.url = {
                'file_path': os.path.join(post.public_id.hex, f'{media_item.public_id.hex}{file_extension}'),
                'original_file_name': file_name
            }
            media_item.state = 'CREATED'
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
