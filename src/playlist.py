import isodate
from googleapiclient.discovery import build
import datetime


class PlayList:

    def __init__(self, id: str):
        self.id = id
        self.title = None
        self.url = None
        self.playlist_videos = None
        self.api_key = "AIzaSyAUQCAV98IhpxiAFMP_Luu-mpicoI3JUGc"
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.best_video_url = None

        self.get_playlist_info()

    def get_playlist_info(self):
        playlist_info = self.youtube.playlists().list(part='snippet', id=self.id).execute()
        self.playlist_videos = playlist_info
        self.title = playlist_info['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.id}"

    @property
    def total_duration(self):
        info = self.youtube.playlistItems().list(playlistId=self.id,
                                                 part='contentDetails',
                                                 maxResults=50,
                                                 ).execute()

        duration = 0
        for video in info['items']:
            video_duration = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=video['contentDetails']['videoId']
                                                        ).execute()
            duration += isodate.parse_duration(video_duration['items'][0]['contentDetails']['duration']).total_seconds()
        return datetime.timedelta(seconds=duration)

    def show_best_video(self):

        like_count = 0
        max_likes = 0
        url = ''
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        for video in video_response['items']:

            like_count = int(video['statistics']['likeCount'])
            if like_count > max_likes:
                url = ''.join(['https://youtu.be/', video['id']])
                max_likes = like_count
            self.best_video_url = url

        return url


if __name__ == '__main__':
    pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')

    pl.show_best_video()

    # assert pl.show_best_video() == "https://youtu.be/cUGyMzWQcGM"
