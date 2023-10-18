import os
from googleapiclient.discovery import build


class Video:
    api_key = None

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.title = None
        self.url = None
        self.view_count = None
        self.like_count = None
        self.api_key = os.getenv('YOUTUBE_ANALYTICS_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

        self.get_video_info()

    def __str__(self):
        return self.title

    def get_video_info(self):
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=self.video_id
                                                    ).execute()
        self.title = video_response['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/watch?v={self.video_id}"
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.title = None
        self.url = None
        self.view_count = None
        self.like_count = None
        self.playlist_id = playlist_id

        self.get_video_info()
