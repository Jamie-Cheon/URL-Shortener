from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, settings
from users.serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False)
    def logout(self, request):
        # permission_classes = (AllowAny,)
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)

        response = Response({"detail": "Successfully logged out."},
                            status=status.HTTP_200_OK)
        return response
