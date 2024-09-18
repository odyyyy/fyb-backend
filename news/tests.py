from unittest.mock import patch

from django.urls import reverse
from rest_framework.test import APITestCase

from news.services import get_news_item


def get_actual_news_mocked():
    return [
        {
            "title": "Test news",
            "slug": "test-news",
            "description": "bla bla bla",
            "pubDate": "2024-09-18 17:09:09",
            "image": "https://media.pitchfork.com/photos/66eaeb47d2a9f24c73617a27/master/pass/Haley-Heynderickx.jpg"
        },
        {
            "title": "Test news 2",
            "slug": "test-news-2",
            "description": "bla bla bla 2",
            "pubDate": "2024-09-18 17:09:09",
            "image": "https://media.pitchfork.com/photos/66eaeb47d2a9f24c73617a27/master/pass/Haley-Heynderickx.jpg"
        }
    ]


def get_news_item_mocked(slug: str):
    news = get_actual_news_mocked()
    for item in news:
        if item['slug'] == slug:
            return item

class NewsTestCase(APITestCase):


    @patch('news.views.get_actual_news', get_actual_news_mocked)
    def test_news_list(self):
        response = self.client.get(reverse('news-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    @patch('news.views.get_news_item', get_news_item_mocked)
    def test_news_detail(self):
        response = self.client.get(reverse('news-detail', kwargs={'slug': 'test-news'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Test news')

    @patch('news.views.get_news_item', get_news_item_mocked)
    def test_news_detail_not_found(self):
        response = self.client.get(reverse('news-detail', kwargs={'slug': 'test-news-not-found'}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'error': 'Новость не найдена'})

