from django.db import models


class WebhookEvent(models.Model):
    """Model to store incoming webhook events."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    source = models.CharField(max_length=100, help_text="Source of the webhook (e.g., 'slack', 'stripe', 'github')")
    payload = models.JSONField(help_text="The webhook payload data")
    received_at = models.DateTimeField(auto_now_add=True, help_text="When the webhook was received")
    processed_at = models.DateTimeField(null=True, blank=True, help_text="When the webhook was processed")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True, help_text="Error message if processing failed")
    
    class Meta:
        ordering = ['-received_at']
        verbose_name = 'Webhook Event'
        verbose_name_plural = 'Webhook Events'
    
    def __str__(self):
        return f"{self.source} - {self.received_at.strftime('%Y-%m-%d %H:%M:%S')} - {self.status}"
