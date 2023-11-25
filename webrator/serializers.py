from rest_framework import serializers

class AnalyticsInputSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)
    code = serializers.CharField(required=False, allow_blank=True)

class PersonaInputSerialier(serializers.Serializer):
    url = serializers.URLField(required=True)
    depth = serializers.CharField(required=False, allow_blank=True)
