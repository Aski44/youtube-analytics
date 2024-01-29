import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def __str__(self):
        """Строковое представление экземпляра по шаблону `<название_канала> (<ссылка_на_канал>)`"""
        return f"{self.title} ('{self.url}')"

    def __add__(self, other):
        """Возвращает сумму числа подписчиков"""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """Возвращает разницу числа подписчиков"""
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        """Возвращает True или False, если подписчиков >"""
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        """Возвращает True или False, если подписчиков >="""
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        """Возвращает True или False, если подписчиков <"""
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        """Возвращает True или False, если подписчиков <="""
        return int(self.subscriber_count) <= int(other.subscriber_count)

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

    def to_json(self, file):
        """
        Сохраняет в файл значения атрибутов экземпляра
        """
        data = {
            "channel_id": self.__channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


