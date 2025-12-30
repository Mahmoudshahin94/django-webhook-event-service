from django.contrib import admin
from .models import WebhookEvent


@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'source', 'status', 'received_at', 'processed_at']
    list_filter = ['status', 'source', 'received_at']
    search_fields = ['source', 'payload']
    readonly_fields = ['received_at', 'processed_at']
    date_hierarchy = 'received_at'
