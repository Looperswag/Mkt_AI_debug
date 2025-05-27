import os
import yt_dlp
from models import Video, Audio, Metadata, Comment, Text
import re

cookies_path = '/opt/ai_workspace/Yingpeng/Mkt_AI内容审核/TT/cookies.txt'


class TikTokDataCollector:
    def __init__(self):
        pass

    def get_video_data(self, url):
        """
        Fetch video data using yt_dlp.

        Args:
            url (str): The TikTok video URL.

        Returns:
            dict: A dictionary containing video information.
        """
        try:
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'quiet': True,  # Suppress unnecessary output
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(url, download=False)  # Get video info without downloading
                return video_info

        except Exception as e:
            print(f"An error occurred while fetching video data: {e}")
            return None





class TikTokVideoCollector(TikTokDataCollector):
    def collect(self, url, download_path=None):
        try:
            print(f"Starting collection for video URL: {url}")

            # Set download path
            if not download_path:
                download_path = os.path.join(os.getcwd(), 'videos')
            os.makedirs(download_path, exist_ok=True)

            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': os.path.join(download_path, '%(id)s.%(ext)s'),
            }

### INS video test
#            ydl_opts = {
#                'format': 'bestvideo+bestaudio/best',
#                'outtmpl': os.path.join(download_path, '%(id)s.%(ext)s'),
                # Adding cookies for INS video download
                #'cookies': cookies_path,
                #Instead of manually exporting cookies, let yt-dlp fetch them automatically from your browser
#                'cookiesfrombrowser': ('chrome',),  # Change to ('firefox',) or ('edge',) if needed
#                'sleep_interval': 10,  # Helps prevent Instagram rate-limiting
#                'retries': 3,  # Retry if it fails
#            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_path = os.path.join(download_path, f"{info['id']}.mp4")

            # Create Video object
            video_obj = Video(
                id=info['id'],
                downloaded_path=video_path
            )

            # Create Metadata object
            metadata = Metadata(
                id=info['id'],
                title=info['title'],
                length=info['duration'],
                views=info['view_count'],
                author=info['uploader'],
                description=info['description'],
                publish_date=info['upload_date'],
            )

            print(f"Collection successful for video ID: {info['id']}")
            return video_obj, metadata

        except Exception as e:
            print(f"An error occurred during collection: {e}")
            return None


