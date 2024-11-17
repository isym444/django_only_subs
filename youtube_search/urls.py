"""
URL configuration for youtube_search project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from channel_search import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.search_channel, name='search_channel'),
    path('delete/<int:search_id>/', views.delete_search, name='delete_search'),
    path('add-channel/', views.add_channel, name='add_channel'),
    path('update-all-channels/', views.update_all_channels, name='update_all_channels'),
    path('mark-viewed/<int:channel_id>/', views.mark_video_viewed, name='mark_video_viewed'),
]
