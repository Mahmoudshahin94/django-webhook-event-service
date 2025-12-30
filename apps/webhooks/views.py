from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import WebhookEvent
from .serializers import WebhookEventSerializer
from .tasks import process_webhook_event


class WebhookReceiveView(APIView):
    """API endpoint to receive webhook events."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Receive a webhook event, store it, and queue it for processing.
        """
        # Extract source from query params or payload
        source = request.query_params.get('source', request.data.get('source', 'unknown'))
        
        # Create webhook event
        webhook_event = WebhookEvent.objects.create(
            source=source,
            payload=request.data
        )
        
        # Queue the event for processing (async)
        process_webhook_event.delay(webhook_event.id)
        
        return Response({
            'message': 'Webhook received successfully',
            'event_id': webhook_event.id,
            'status': 'queued'
        }, status=status.HTTP_200_OK)


class WebhookListView(generics.ListAPIView):
    """API endpoint to list all webhook events."""
    queryset = WebhookEvent.objects.all()
    serializer_class = WebhookEventSerializer
    permission_classes = [IsAuthenticated]


class WebhookDetailView(generics.RetrieveAPIView):
    """API endpoint to retrieve a specific webhook event."""
    queryset = WebhookEvent.objects.all()
    serializer_class = WebhookEventSerializer
    permission_classes = [IsAuthenticated]
