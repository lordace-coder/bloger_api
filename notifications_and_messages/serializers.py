from rest_framework import serializers

from .models import Messages, Notifications

# * definition helpers
ModelSerializer = serializers.ModelSerializer
MethodField = serializers.SerializerMethodField



class NotificationSerializer(ModelSerializer):
    username = serializers.CharField(source='user.username',read_only=True)
    class Meta:
        model = Notifications
        fields = (
            'notification',
            'user',
            'username',
            'read',
            'formated_time'
        )

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Messages
        exclude = ['id']