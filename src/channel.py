import json
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YOUTUBE_ANALYTICS_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.title = None
        self.description = None
        self.url = None
        self.subscriber_count = None
        self.video_count = None
        self.view_count = None

        self.get_channel_info()

    def __str__(self):
        """Возвращает название и ссылку на канал по шаблону `<название_канала> (<ссылка_на_канал>)`"""
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)

    def get_channel_info(self):
        """Получает информацию о канале с помощью YouTube API и заполняет атрибуты данными"""
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        if 'items' in channel and len(channel['items']) > 0:
            item = channel['items'][0]
            snippet = item['snippet']
            statistics = item['statistics']
            self.title = snippet['title']
            self.description = snippet['description']
            self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
            self.subscriber_count = statistics['subscriberCount']
            self.video_count = statistics['videoCount']
            self.view_count = statistics['viewCount']

    @property
    def channel_id(self):
        """Геттер для атрибута channel_id"""
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, new__channel_id):
        """Сеттер для атрибута channel_id"""
        self.__channel_id = new__channel_id
        # После изменения channel_id, обновляем информацию о канале
        self.get_channel_info()

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return youtube

    def to_json(self, filename):
        """Сохраняет значения атрибутов экземпляра Channel в файл в формате JSON"""
        data = {
            'id': f'{self.__channel_id}',
            'title': f'{self.title}',
            'description': f'{self.description}',
            'url': f'{self.url}',
            'subscriber_count': f'{self.subscriber_count}',
            'video_count': f'{self.video_count}',
            'view_count': f'{self.view_count}',
        }
        with open(filename, 'w') as file:
            json.dump(data, file)

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))
