from django.db import models

class ChannelSearch(models.Model):
    channel_name = models.CharField(max_length=200)
    channel_id = models.CharField(max_length=100)
    video_id = models.CharField(max_length=50)
    video_title = models.CharField(max_length=500)
    video_views = models.CharField(max_length=100)
    upload_date = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    has_new_video = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.channel_name} - {self.video_title}"
