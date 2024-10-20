from debug_toolbar import urls as debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include, re_path

from users.views import auth

api_patterns = [
    path('vacancies/', include('vacancies.urls')),
    path('bands/', include('bands.urls')),
    path('users/', include('users.urls')),
    path('news/', include('news.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/v1/', include((api_patterns, 'api'), namespace='api')),

    re_path('', include('social_django.urls', namespace='social')),
    path('auth/', auth),
    path('djdt/', include(debug_toolbar_urls)),
]
