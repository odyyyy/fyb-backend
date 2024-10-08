from rest_framework.response import Response
from rest_framework.views import APIView

from news.services import get_actual_news, get_news_item


class NewsListView(APIView):
    def get(self, request):
        news_data = get_actual_news()
        return Response(news_data)


class NewsDetailView(APIView):
    def get(self, request, slug):
        news_item_data = get_news_item(slug)
        if news_item_data is not None:
            return Response(news_item_data)
        return Response({'error': 'Новость не найдена'}, status=404)
