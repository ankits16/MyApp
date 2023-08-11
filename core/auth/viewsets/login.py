from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from core.auth.serializers import LoginSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class LoginViewSet(ViewSet):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    @swagger_auto_schema(
        operation_description="Login API",
        request_body=LoginSerializer,
        responses={
            status.HTTP_200_OK: "Successful response",
            status.HTTP_400_BAD_REQUEST: "Bad request",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)