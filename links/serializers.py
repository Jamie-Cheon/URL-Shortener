from rest_framework import serializers
from .models import Link


class LinkSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    short_url = serializers.ReadOnlyField()

    class Meta:
        model = Link
        fields = ('id', 'origin_url', 'short_url', 'created', 'owner')

