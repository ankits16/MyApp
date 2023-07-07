from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.abstract.serializers import AbstractSerializer
from core.post.models import Post
from core.user.models import User
from core.user.serializers import UserSerializer

class PostSerializer(AbstractSerializer):
    # this is to ensure that public_id of the user is returned instead of complet user object
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='public_id')
    liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    #Django Rest Framework, the framework relies on certain naming conventions for serializer validation methods to work properly. 
    #By default, Django Rest Framework expects validation methods to be named in the format 
    #validate_<field_name>, where <field_name> 
    #is the name of the field being validated.
    def validate_author(self, value):
        #n Django Rest Framework, the self.context["request"] refers to the HTTP request object associated with the serializer. 
        # It provides access to various details and data related to the current request being processed
        if self.context["request"].user != value:
            raise ValidationError("Cannot create post for another user.")
        return value
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(rep['author'])
        rep['author'] = UserSerializer(author).data
        return rep
    
    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True 
        instance = super().update(instance, validated_data)
        return instance
    
    def get_liked(self, instance):
        request = self.context.get('request', None)
        if request is None or request.user.is_anonymous:
            return False
        return request.user.has_liked(instance)
    
    def get_likes_count(self, instance):
        return instance.liked_by.count()
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'body', 'edited', 'liked', 'likes_count', 'created', 'updated']
        read_only_fields = ['edited']