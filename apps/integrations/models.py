from django.db import models


class Process(models.Model):
    """Model to store process scripts for backup."""
    
    name = models.CharField(max_length=50, help_text="Process name")
    code = models.CharField(max_length=100, unique=True, help_text="Unique process code (used as filename)")
    script = models.TextField(help_text="Python script content")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['code']
        verbose_name = 'Process'
        verbose_name_plural = 'Processes'
    
    def __str__(self):
        return f"{self.code} - {self.name}"
