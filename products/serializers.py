from rest_framework import serializers
from core.abstract.serializers import AbstractSerializer
from .models import Product

class ProductSerializer(AbstractSerializer):
    class Meta:
        model = Product
        fields = ['public_id','title', 'image', 'likes']
        read_only_fields = ['likes']