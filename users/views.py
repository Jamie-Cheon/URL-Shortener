from django.contrib.auth import logout as django_logout, login, authenticate
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, settings, serializers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.fields import CharField

from users.serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token': token.key, 'user_id': user.pk}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # @action(detail=False)
    # def logout(self, request):
    #     # permission_classes = (AllowAny,)
    #     try:
    #         request.user.auth_token.delete()
    #     except (AttributeError, ObjectDoesNotExist):
    #         return Response({"detail": "Not authorized User."},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #     if getattr(settings, 'REST_SESSION_LOGIN', True):
    #         django_logout(request)
    #         return Response({"detail": "Successfully logged out."},
    #                         status=status.HTTP_200_OK)
