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


class Serializer:
    def __init__(self, fields):
        self.fields = fields

    def getSerializedItems(self, items):
        items_serialized = []
        for p in items:
            item_dict = {}
            for f in self.fields:
                item_dict[f] = getattr(p, f)
            items_serialized.append(item_dict)
        return items_serialized

    def getSerializedItem(self, item):
        item_dict = {}
        for f in self.fields:
            item_dict[f] = getattr(item, f)
        return item_dict


class PostsSerializer(Serializer):
    def getSerializedItems(self, items):
        items_serialized = []
        for p in items:
            item_dict = {}
            for f in self.fields:
                item_dict[f] = getattr(p, f)
            item_dict['username'] = p.user.username
            items_serialized.append(item_dict)
        return items_serialized

    def getSerializedItem(self, item):
        item_dict = super().getSerializedItem(item)
        item_dict['username'] = item.user.username
        return item_dict
