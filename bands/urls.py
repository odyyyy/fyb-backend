from django.urls import path
from rest_framework.routers import SimpleRouter

from bands.views import BandAPIView

app_name = 'bands'

urlpatterns = [
    path('', BandAPIView.as_view(actions={'get': 'retrieve', 'post': 'create',
                                  'update': 'partial_update', 'delete': 'destroy'}), name='bands'),
]
