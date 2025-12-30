from django.urls import path
from .views import WebhookReceiveView, WebhookListView, WebhookDetailView

app_name = 'webhooks'

urlpatterns = [
    path('receive/', WebhookReceiveView.as_view(), name='receive'),
    path('list/', WebhookListView.as_view(), name='list'),
    path('<int:pk>/', WebhookDetailView.as_view(), name='detail'),
]

