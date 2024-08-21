from django.urls import path, include
from rest_framework.routers import SimpleRouter

from users.views import  UserFavouritesListView

# router = SimpleRouter()
# router.register('favourites', UserFavouritesView, basename='favourites')

urlpatterns = [
    path('favourites/', UserFavouritesListView.as_view()),
    path('favourites/<uuid:uuid>/', UserFavouritesListView.as_view()),
]
