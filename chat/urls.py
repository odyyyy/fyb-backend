from django.urls import path
from .views import  ChatView, chat_test_with_template

urlpatterns = [
    path('', ChatView.as_view(), name='chat'),
    path('test/', chat_test_with_template, name='chat-test'),
]