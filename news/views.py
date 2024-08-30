from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView

import json

from news.services import check_new_actual_news, parse_actual_news, get_actual_news, get_news_item
from rest_framework.response import Response


class NewsListView(APIView):
    def get(self, request):
        check_new_actual_news()
        news_data = get_actual_news()
        return Response(news_data)


class NewsDetailView(APIView):
    def get(self, request, slug):
        news_item_data = get_news_item(slug)
        if news_item_data is not None:
            return Response(news_item_data)
        return Response({'error': 'Новость не найдена'}, status=404)
