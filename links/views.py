from django.shortcuts import redirect
from rest_framework import viewsets
from core.throttling import VIPThrottle, NormalThrottle
from .models import Link
from .serializers import LinkSerializer


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def check_throttles(self, request):
        if self.action == 'create':
            super().check_throttles(request)

    def get_throttles(self):
        if self.request.user.membership == 0:
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
