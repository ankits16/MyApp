from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from core.post.models import Post

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