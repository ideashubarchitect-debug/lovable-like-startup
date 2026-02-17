from django.contrib import admin
from .models import App


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'description')
