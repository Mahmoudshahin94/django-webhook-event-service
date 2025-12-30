from django.contrib import admin
from .models import Process


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'created_at', 'updated_at']
    search_fields = ['code', 'name', 'script']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
