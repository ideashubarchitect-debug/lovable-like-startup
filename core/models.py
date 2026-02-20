from django.conf import settings
from django.db import models
from django.utils.text import slugify


def default_sections():
    return []


class App(models.Model):
    """A user-created app (Lovable/Replit style project)."""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('building', 'Building'),
        ('ready', 'Ready'),
    ]
    TEMPLATE_CHOICES = [
        ('landing', 'Landing Page'),
        ('saas', 'SaaS / Product'),
        ('portfolio', 'Portfolio'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='apps'
    )
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=80, blank=True, unique=True)
    description = models.TextField(
        blank=True,
        help_text='What do you want to build? Describe your app.'
    )
    template = models.CharField(
        max_length=20,
        choices=TEMPLATE_CHOICES,
        default='landing'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    published = models.BooleanField(default=False)
    sections = models.JSONField(default=default_sections, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) if self.name else f'app-{self.pk or 0}'
            if not base or base == 'app-0':
                base = 'app'
            self.slug = base
            idx = 1
            while App.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f'{base}-{idx}'
                idx += 1
        super().save(*args, **kwargs)

    def get_public_url(self, request=None):
        from django.urls import reverse
        path = reverse('core:app_public', kwargs={'slug': self.slug or str(self.pk)})
        if request and request.build_absolute_uri:
            return request.build_absolute_uri(path)
        return path
