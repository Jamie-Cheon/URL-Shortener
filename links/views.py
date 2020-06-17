from rest_framework import viewsets
from rest_framework.response import Response

from .models import Link
from .serializers import LinkSerializer
from django.shortcuts import redirect


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    lookup_field = 'short_url'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return redirect(instance.origin_url)

