import re, os
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from core.post.models import Post
from core.mediaItems.models import MediaItem
from pytube import YouTube

@shared_task
def send_media_items_uploaded_email(post_id, request):
    try:
        post = Post.objects.get(pk=post_id)
        subject = 'Media Items Uploaded'
        template_name = 'email_post.html'
        print(f'data  = {request}')
        context = {
            'post': post,
            'scheme': request.get('scheme'),
            'host': request.get('host'),
            'root' : settings.MEDIA_URL
            }
        message = render_to_string(template_name, context)
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [post.author.email]
        
        print(f'sending email to {recipient_list}')
        send_mail(
            subject, 
            message, 
            from_email, 
            recipient_list, 
            fail_silently=False, 
            html_message=message
            )
    except Post.DoesNotExist:
        pass  # Handle the case where the post does not exist


@shared_task
def download_associated_youtube_video(post_id):
    try:
        
        post = Post.objects.get(pk=post_id)
        print(f'Downloading video {post.public_id.hex}')
        youtube_urls = re.findall(r'https?://(?:www\.|m\.)?youtube\.com/(?:watch\?v=[\w-]+|shorts/[\w-]+)', post.body)
        
        for url in youtube_urls:
            youtube = YouTube(url)
            video_stream = youtube.streams.get_highest_resolution()
            
            # Create a folder based on the public_id (without '-')
            folder_name = str(post.public_id).replace('-', '')
            download_path = os.path.join(settings.MEDIA_ROOT, folder_name)
            
            # Create the folder if it doesn't exist
            os.makedirs(download_path, exist_ok=True)
            
            # Download the video
            video_extension = video_stream.mime_type.split('/')[1]
            media_item = MediaItem.objects.create(
                post=post,
                type='video',
                state='UPLOADED'
            )
            video_filename = f"{media_item.public_id.hex}.{video_extension}"
            video_path = os.path.join(download_path, video_filename)
            video_stream.download(output_path=download_path, filename=video_filename)
            
            # Update the URL field of the MediaItem
            media_item.url = {'file_path':  os.path.join(folder_name, video_filename)}
            media_item.save()
            
    except Post.DoesNotExist:
        pass  # Handle