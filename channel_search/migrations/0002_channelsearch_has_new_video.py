# Generated by Django 5.1.3 on 2024-11-17 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("channel_search", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="channelsearch",
            name="has_new_video",
            field=models.BooleanField(default=False),
        ),
    ]