from django.conf import settings
from django.db import models


class App(models.Model):
    """A user-created app (Lovable/Replit style project)."""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('building', 'Building'),
        ('ready', 'Ready'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='apps'
    )
    name = models.CharField(max_length=120)
    description = models.TextField(
        blank=True,
        help_text='What do you want to build? Describe your app.'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
