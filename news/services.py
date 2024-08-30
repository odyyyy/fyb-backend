from datetime import datetime

import requests
from xml.dom.minidom import parseString, Document
import json
from django.utils.text import slugify

NEWS_RSS_URL = "https://pitchfork.com/feed/feed-news/rss"

def parse_actual_news(news_document: Document) -> None:

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

    with open('news_data.json', 'w') as file:
        json.dump(json_news, file)


def check_new_actual_news() -> None:
    rss_response = requests.get(NEWS_RSS_URL)
    news_document = parseString(rss_response.content)
    last_news_title = news_document.getElementsByTagName("item")[0].getElementsByTagName("title")[0].firstChild.data

    with open('news_data.json', 'r') as file:
        news_data = json.load(file)
        if news_data[0]['title'] != last_news_title:
            parse_actual_news(news_document)


def get_actual_news() -> list:
    with open('news_data.json', 'r') as file:
        news_data = json.load(file)
        return news_data

def get_news_item(slug: str) -> dict:
    with open('news_data.json', 'r') as file:
        news_data = json.load(file)
        for news_item in news_data:
            if news_item['slug'] == slug:
                return news_item
