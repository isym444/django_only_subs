from django.contrib import admin
from django.urls import path
from channel_search import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.search_channel, name='search_channel'),
] 