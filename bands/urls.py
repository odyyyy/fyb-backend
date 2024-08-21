from django.urls import path
from rest_framework.routers import SimpleRouter

from bands.views import BandAPIView

router = SimpleRouter()

router.register('', BandAPIView, basename='bands')
urlpatterns = router.urls
