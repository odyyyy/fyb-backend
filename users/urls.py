from django.urls import path, include
from rest_framework.routers import SimpleRouter

from users.views import UserFavouritesView, UsersVacancyView, UserProfileView

router = SimpleRouter()
router.register('favourites', UserFavouritesView, basename='favourites')
router.register('vacancies', UsersVacancyView, basename='users-vacancies')
urlpatterns = router.urls + [
    path('profile/', UserProfileView.as_view()),
]