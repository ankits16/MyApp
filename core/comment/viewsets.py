from django.http.response import Http404
from rest_framework.response import Response
from rest_framework import status
from core.abstract.viewsets import AbstractViewSet
from core.comment.models import Comment
from core.comment.serializers import CommentSerializer
from core.auth.permissions import UserPermission

class CommentViewSet(AbstractViewSet):
    http_method_names = ('post', 'delete', 'get', 'put')
    permission_classes = (UserPermission,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Comment.objects.all()
        post_pk = self.kwargs['post_pk']
        if post_pk is None:
            return Http404
        #In this context, post__public_id is a Django ORM (Object-Relational Mapping) syntax 
        # that allows you to specify a relationship between models and filter based on related fields. 
        # The double underscore (__) is used to traverse relationships and access fields of related models.
        # Assuming there is a foreign key relationship between the Comment model and the Post model, 
        # where a comment belongs to a post, the post__public_id filter condition will filter 
        # the comments based on the public_id field of the related post.
        queryset = Comment.objects.filter(post__public_id=post_pk)
        return queryset
    
    def get_object(self):
        obj = Comment.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    # def create(self, request, *args, **kwargs):
    #     print("Creating comment...")
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(serializer.data,  status=status.HTTP_201_CREATED)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    