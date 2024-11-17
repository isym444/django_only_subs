from django.contrib import admin
from .models import ChannelSearch

@admin.register(ChannelSearch)
class ChannelSearchAdmin(admin.ModelAdmin):
    list_display = ('channel_name', 'video_title', 'created_at')
    search_fields = ('channel_name', 'video_title')
    list_filter = ('created_at',)
