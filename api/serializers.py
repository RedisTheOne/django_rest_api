from rest_framework import serializers
from api.models import User, Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']


class UserSignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class FilteredUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class PostSerializer(serializers.ModelSerializer):
    # user = FilteredUserSerializer(read_only=True)
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_at', 'username']


class CommentSerializer(serializers.ModelSerializer):
    postId = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Comment
        fields = ['id', 'text', 'postId', 'username']
