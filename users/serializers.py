from action_serializer import ModelActionSerializer
from .models import User
from rest_framework import serializers
from links.serializers import LinkSerializer


class UserSerializer(ModelActionSerializer):
    urls = LinkSerializer(many=True, read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    membership = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'membership', 'urls',)
        action_fields = {
            'login': {'fields': ('email', 'password')},
            'update': {'fields': ('email', 'username')},
        }

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user


