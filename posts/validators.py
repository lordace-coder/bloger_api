from rest_framework import serializers

from posts.models import Post


def validate_title(value):
    query = Post.objects.filter(title__iexact=value)
    if query.exists():
        raise serializers.ValidationError("Post with title already exists")
    return value
