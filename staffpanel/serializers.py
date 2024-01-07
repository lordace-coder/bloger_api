from rest_framework import serializers

ModelSerializer = serializers.ModelSerializer
SMF = serializers.SerializerMethodField
CharField = serializers.CharField



class ActionSerializer(ModelSerializer):
    
    class Meta:
        ...