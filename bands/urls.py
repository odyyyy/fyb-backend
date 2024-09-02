from django.urls import path
from rest_framework.routers import SimpleRouter

from bands.views import BandAPIView


app_name = 'bands'
router = SimpleRouter()

router.register('', BandAPIView, basename='band')
urlpatterns = router.urls
