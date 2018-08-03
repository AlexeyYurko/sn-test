from rest_framework import serializers

from soc.models import User, Post


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'admin', 'staff', 'is_active')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'text', 'image', 'rating', 'by_user', 'created_at', 'visible')
