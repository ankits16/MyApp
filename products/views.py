from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status

# Create your views here.
class ProductViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="list of all products",
        responses={
            status.HTTP_200_OK: "Success",
            status.HTTP_400_BAD_REQUEST: "Bad request",
        }
    )
    def list(self, request):# /api/products
        products= Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="create a product",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'image': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['title', 'image'],
        ),
        responses={
            status.HTTP_201_CREATED: "Successful creation",
            status.HTTP_400_BAD_REQUEST: "Bad request",
        }
    )
    def create(self, request):#/api/products
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request):#/api/products/<str: id>
        pass

    def update(self, request):#/api/products/<str: id>
        pass

    def destroy(self, request):#/api/products
        pass
