from rest_framework.routers import SimpleRouter

from .views import VacancyViewSet

router = SimpleRouter()
router.register('', basename='vacancies', viewset=VacancyViewSet)
urlpatterns = router.urls

