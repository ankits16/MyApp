from pytube import YouTube

#

# URL of the YouTube video you want to download
video_url = "https://www.youtube.com/shorts/ll6OeUgaNqE"

# Create a YouTube object
youtube = YouTube(video_url)

# Get the highest resolution stream (usually the best quality)
video_stream = youtube.streams.get_highest_resolution()

# Specify the directory where you want to save the downloaded video
download_path = "/Users/ankit/Documents/code/web learnings/django/myapp/uploaded_media_items/yt"

# Download the video
video_stream.download(output_path=download_path)

print("Video downloaded successfully.")




