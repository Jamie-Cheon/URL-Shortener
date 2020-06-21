from django.shortcuts import redirect
from rest_framework import viewsets

from core.permissions import CustomLinkPermission
from core.throttling import VIPThrottle, NormalThrottle, AnonThrottle
from .models import Link
from .serializers import LinkSerializer


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = (CustomLinkPermission,)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            serializer.save()

    def check_throttles(self, request):
        if self.action == 'create':
            super().check_throttles(request)

    def get_throttles(self):
        if self.request.user.is_anonymous:
            return [AnonThrottle()]
        elif self.request.user.membership == 0:
            return [VIPThrottle()]
        else:
            return [NormalThrottle()]


class RedirectViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    lookup_field = 'short_url'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Link.clicked(self=instance)
        return redirect(instance.origin_url)
