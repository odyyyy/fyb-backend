from datetime import datetime

import requests
from xml.dom.minidom import parseString, Document
import json
from django.utils.text import slugify
from django.core.cache import cache

NEWS_RSS_URL = "https://pitchfork.com/feed/feed-news/rss"
NEWS_CACHE_KEY = 'news'


def parse_actual_news() -> None:
    rss_response = requests.get(NEWS_RSS_URL)
    news_document = parseString(rss_response.content)

    news_items = news_document.getElementsByTagName("item")
    json_news = []
    for item in news_items:
        title = item.getElementsByTagName("title")[0].firstChild.data
        slug = slugify(title)

        pub_date_str = item.getElementsByTagName("pubDate")[0].firstChild.data
        pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z").strftime("%Y-%m-%d %H:%M:%S")

        description = item.getElementsByTagName("description")[0].firstChild.data
        image = item.getElementsByTagName("media:thumbnail")[0].getAttribute("url")

        json_news.append({
            "title": title,
            "slug": slug,
            "description": description,
            "pubDate": pub_date,
            "image": image,
        })

    json_news.reverse()
    cache.set(NEWS_CACHE_KEY, json_news, 60 * 60)


def get_news_item(slug: str) -> dict:
    news_data = cache.get(NEWS_CACHE_KEY)
    if news_data is not None:
        for item in news_data:
            if item['slug'] == slug:
                return item


def get_actual_news() -> list:
    news_data = cache.get(NEWS_CACHE_KEY)
    if news_data is not None:
        return news_data
    parse_actual_news()
    get_actual_news()

