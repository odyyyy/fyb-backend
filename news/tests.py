from unittest.mock import patch

from django.urls import reverse
from rest_framework.test import APITestCase

from news.services import parse_actual_news


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


class NewsAPITestCase(APITestCase):

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


class NewsServiceTestCase(APITestCase):

    @patch('news.services.requests.get')
    # @patch('news.services.cache.set')
    def test_parse_actual_news(self, mock_request_get_data):
        mock_rss_content = '''<rss
	xmlns:atom="http://www.w3.org/2005/Atom"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:media="http://search.yahoo.com/mrss/" version="2.0">
	<channel>
		<title>RSS: News</title>
		<description>News content RSS feed</description>
		<item>
			<title>Test News</title>
			<link>https://test.com</link>
			<guid isPermaLink="false">66ec8440c7576e9238fa659a</guid>
			<pubDate>Thu, 19 Sep 2024 20:53:34 +0000</pubDate>
			<media:content/>
			<description>This is a test news item.</description>
			<category>News</category>
			<media:keywords>Film</media:keywords>
			<dc:creator>Madison Bloom</dc:creator>
			<dc:publisher>Condé Nast</dc:publisher>
			<media:thumbnail url="http://example.com/image.jpg" width="3000" height="1500"/>
		</item>
	</channel>
</rss>'''

        mock_request_get_data.return_value.content = mock_rss_content

        result_json_news = parse_actual_news()

        expected_news = [{
            'title': 'Test News',
            'slug': 'test-news',
            'description': 'This is a test news item.',
            'pubDate': '2024-09-19 20:53:34',
            'image': 'http://example.com/image.jpg',
        }]

        self.assertEqual(result_json_news, expected_news)
