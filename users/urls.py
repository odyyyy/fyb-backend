from django.urls import path, include
from rest_framework.routers import SimpleRouter

from users.views import UserFavouritesView

router = SimpleRouter()
router.register('favourites', UserFavouritesView, basename='favourites')
urlpatterns = router.urls
