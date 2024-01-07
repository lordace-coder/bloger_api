from django.contrib.auth.models import User
from rest_framework import serializers


def validate_email(value):
    query = User.objects.filter(email__iexact=value)
    if query.exists():
        raise serializers.ValidationError("Account with this email address already exists")
    if '@' not in value:
        raise serializers.ValidationError("Invalid email address")
    return value
