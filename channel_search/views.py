from django.shortcuts import render, redirect
import aiotube
from .models import ChannelSearch
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import datetime
from time import sleep

def search_channel(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        channel_name = request.POST.get('channel_name')
        print(f"Received search request for channel: {channel_name}")
        
        try:
            search_results = []
            channels = aiotube.Search.channels(channel_name, 2)
            
            for channel_id in channels:
                try:
                    channel = aiotube.Channel(channel_id)
                    metadata = channel.metadata
                    
                    search_results.append({
                        'channel_id': channel_id,
                        'name': metadata['name'],
                        'subscriber_count': metadata['subscribers'],
                        'description': metadata.get('description', 'No description available')[:200] + '...'
                    })
                except Exception as e:
                    print(f"Error processing channel {channel_id}: {e}")
                    continue
            
            html = render_to_string('channel_search/search_results.html', {
                'search_results': search_results
            }, request=request)
            
            return JsonResponse({
                'status': 'success',
                'html': html
            })
            
        except Exception as e:
            print(f"Top-level error occurred: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    # Regular page load
    return render(request, 'channel_search/search.html', {
        'saved_searches': ChannelSearch.objects.all()
    })

def add_channel(request):
    if request.method == 'POST':
        channel_id = request.POST.get('channel_id')
        print(f"Received POST data: {request.POST}")  # Debug all POST data
        print(f"Received channel_id: {channel_id}")   # Debug channel_id
        
        if not channel_id:
            return JsonResponse({'status': 'error', 'message': 'No channel ID provided'})
            
        try:
            # Get channel data
            channel = aiotube.Channel(channel_id)
            if not channel or not channel.metadata:
                return JsonResponse({'status': 'error', 'message': 'Could not fetch channel metadata'})
                
            channel_data = channel.metadata
            
            # Get latest video ID with error handling
            latest_video = channel.last_uploaded
            print(f"Latest video: {latest_video}")
            
            # Create channel search entry with minimal data if video fetch fails
            try:
                video = aiotube.Video(latest_video)
                video_data = video.metadata if video and video.metadata else {}
            except Exception as video_error:
                print(f"Error fetching video data: {video_error}")
                video_data = {}
            
            # Save to database with fallback values
            search_obj = ChannelSearch.objects.create(
                channel_name=channel_data.get('name', 'Unknown Channel'),
                channel_id=channel_id,
                video_id=latest_video or '',
                video_title=video_data.get('title', 'Video information unavailable'),
                video_views=str(video_data.get('views', 'N/A')),
                upload_date=str(video_data.get('upload_date', 'N/A'))
            )
            
            print(f"About to save channel_id: {channel_id}")
            
            return JsonResponse({'status': 'success'})
            
        except Exception as e:
            print(f"Error in add_channel: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f'Error processing channel: {str(e)}'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def delete_search(request, search_id):
    if request.method == 'POST':
        try:
            search = ChannelSearch.objects.get(id=search_id)
            search.delete()
            # Return the search_id in the response so we can use it in JavaScript
            return JsonResponse({'status': 'success', 'search_id': search_id})
        except ChannelSearch.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Search not found'}, status=404) 

def update_all_channels(request):
    if request.method == 'POST':
        try:
            channels = ChannelSearch.objects.all()
            updated_channels = []
            
            print(f"Starting update check for {len(channels)} channels")
            
            for channel_search in channels:
                print(f"\nChecking channel: {channel_search.channel_name} (ID: {channel_search.channel_id})")
                try:
                    # Get channel data
                    channel = aiotube.Channel(channel_search.channel_id)
                    if not channel or not channel.metadata:
                        print(f"❌ Could not fetch metadata for channel {channel_search.channel_id}")
                        continue

                    # Get latest video ID with proper error handling
                    latest_video = channel.last_uploaded
                    print(f"Current stored video ID: {channel_search.video_id}")
                    print(f"Latest video ID found: {latest_video}")
                    
                    if not latest_video:
                        print(f"❌ No latest video found for channel {channel_search.channel_id}")
                        continue

                    if latest_video != channel_search.video_id:
                        print(f"🔄 New video detected for {channel_search.channel_name}")
                        try:
                            video = aiotube.Video(latest_video)
                            video_data = video.metadata if video and video.metadata else {}
                            
                            # Update channel with new video information
                            channel_search.video_id = latest_video
                            channel_search.video_title = video_data.get('title', 'Video information unavailable')
                            channel_search.video_views = str(video_data.get('views', 'N/A'))
                            channel_search.upload_date = str(video_data.get('upload_date', 'N/A'))
                            channel_search.has_new_video = True
                            channel_search.save()
                            
                            updated_channels.append(channel_search.id)
                            print(f"✅ Successfully updated {channel_search.channel_name} with new video: {channel_search.video_title}")
                            
                            sleep(0.5)  # Rate limiting
                            
                        except Exception as video_error:
                            print(f"❌ Error fetching video data for channel {channel_search.channel_id}: {video_error}")
                            continue
                    else:
                        print(f"ℹ️ No new video for {channel_search.channel_name}")
                            
                except Exception as channel_error:
                    print(f"❌ Error processing channel {channel_search.channel_id}: {channel_error}")
                    continue
            
            print(f"\nUpdate complete. Updated {len(updated_channels)} channels")
            
            try:
                return JsonResponse({
                    'status': 'success',
                    'updated_channels': updated_channels
                })
            except ConnectionAbortedError:
                print("❌ Client disconnected before response could be sent")
                return JsonResponse({'status': 'error', 'message': 'Client disconnected'})
            
        except Exception as e:
            print(f"❌ Error in update_all_channels: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def mark_video_viewed(request, channel_id):
    if request.method == 'POST':
        try:
            channel = ChannelSearch.objects.get(id=channel_id)
            channel.has_new_video = False
            channel.save()
            return JsonResponse({'status': 'success'})
        except ChannelSearch.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Channel not found'}, status=404) 