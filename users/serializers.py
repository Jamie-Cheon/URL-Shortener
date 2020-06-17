from django.contrib.auth.models import User
from rest_framework import serializers
from links.serializers import LinkSerializer


class UserSerializer(serializers.ModelSerializer):
    urls = LinkSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'urls',)

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user
