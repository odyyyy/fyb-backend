from unittest.mock import patch, MagicMock

from django.urls import reverse
from rest_framework.test import APITestCase

from news.services import parse_actual_news, NEWS_CACHE_KEY, get_news_item, get_actual_news


def get_news_mock():
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
    news = get_news_mock()
    for item in news:
        if item['slug'] == slug:
            return item


class NewsAPITestCase(APITestCase):

    @patch('news.views.get_actual_news', get_news_mock)
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

    @patch('news.services.requests')
    @patch('news.services.cache.set')
    def test_parse_actual_news(self, mock_cache_set, mock_requests):
        rss_content = '''<rss
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

        mock_response = MagicMock()

        mock_response.status_code = 200
        mock_response.content = rss_content

        mock_requests.get.return_value = mock_response

        result_json_news = parse_actual_news()

        expected_news = [{
            'title': 'Test News',
            'slug': 'test-news',
            'description': 'This is a test news item.',
            'pubDate': '2024-09-19 20:53:34',
            'image': 'http://example.com/image.jpg',
        }]

        mock_cache_set.assert_called_once_with(NEWS_CACHE_KEY, expected_news, 60 * 60)
        self.assertEqual(result_json_news, expected_news)

    @patch('news.services.requests')
    def test_parse_actual_news_failed(self, mock_requests):
        mock_response = MagicMock(status_code=500)
        mock_requests.get.return_value = mock_response

        self.assertEqual(parse_actual_news(),
                         [{'error': f'Failed to get news status code: {mock_response.status_code}'}])

    @patch('news.services.cache.get')
    def test_get_news_item(self, mock_cache_get):
        mock_cache_get.return_value = get_news_mock()

        self.assertEqual(get_news_item('test-news'), {
            'title': 'Test news',
            'slug': 'test-news',
            'description': 'bla bla bla',
            'pubDate': '2024-09-18 17:09:09',
            'image': 'https://media.pitchfork.com/photos/66eaeb47d2a9f24c73617a27/master/pass/Haley-Heynderickx.jpg'
        })

    @patch('news.services.cache.get')
    def test_get_news_item_not_in_cache(self, mock_cache_get):
        mock_cache_get.return_value = None
        self.assertEqual(get_news_item('test-news-not-found'), None)
        mock_cache_get.assert_called_once_with(NEWS_CACHE_KEY)



    @patch('news.services.cache.get')
    def test_get_actual_news(self,mock_cache_get):
        mock_cache_get.return_value = get_news_mock()

        self.assertEqual(get_actual_news(), mock_cache_get.return_value)
        self.assertEqual(mock_cache_get.call_count, 1)


    @patch('news.services.cache.get')
    @patch('news.services.parse_actual_news')
    def test_get_actual_news_not_in_cache(self, mock_parse_actual_news, mock_cache_get):
        mock_cache_get.return_value = None
        mock_parse_actual_news.return_value = get_news_mock()
        result = get_actual_news()

        self.assertEqual(mock_cache_get.call_count, 2)
        self.assertEqual(result, None)

