from rest_framework import serializers
from .models import WebhookEvent


class WebhookEventSerializer(serializers.ModelSerializer):
    """Serializer for webhook events."""
    
    class Meta:
        model = WebhookEvent
        fields = ('id', 'source', 'payload', 'received_at', 'processed_at', 'status', 'error_message')
        read_only_fields = ('id', 'received_at', 'processed_at', 'status', 'error_message')


class WebhookReceiveSerializer(serializers.Serializer):
    """Serializer for receiving webhook payloads."""
    source = serializers.CharField(max_length=100, required=False, default='unknown')
    # Payload can be any JSON data
    # We'll accept it as a dict and validate it's JSON-serializable
    
    def validate(self, attrs):
        # The actual payload will be in request.data
        return attrs

