from rest_framework.routers import DefaultRouter

from .views import VacancyViewSet

router = DefaultRouter()
router.register('', basename='vacancies', viewset=VacancyViewSet)
urlpatterns = router.urls
