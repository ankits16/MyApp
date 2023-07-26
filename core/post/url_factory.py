import os
from django.conf import settings
from django.urls import reverse

class MediaURLFactory:
    def generate_url(self, post_id, media_item_id, file_extension):
        raise NotImplementedError("Subclasses must implement generate_url method.")

class LocalMediaURLFactory(MediaURLFactory):
    def generate_url(self, post_id, media_item_id, file_extension):
        if settings.DEBUG:
            base_url = 'http://localhost:8000'  # Use your local development URL
        else:
            base_url = 'https://example.com'  # Use your production URL

        # Assuming you have a URL pattern like 'media_item_upload' in your 'urls.py'.
        # url_pattern = reverse('media_item_upload', args=[post_id, media_item_id])

        return base_url # f"{base_url}{url_pattern}"
        # return os.path.join(post_media_folder, file_name_with_extension)

class S3MediaURLFactory(MediaURLFactory):
    def generate_url(self, post_id, media_item_id, file_extension):
        # Assuming you use Boto3 for Amazon S3 integration
        # s3_bucket = 'your-s3-bucket-name'
        # file_path = f'media/{str(post_id)}/{media_item_id}{file_extension}'
        # return f"https://{s3_bucket}.s3.amazonaws.com/{file_path}"
        raise NotImplementedError("S3MediaURLFactory is not implemented. Please add your S3 URL generation logic.")