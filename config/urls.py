from debug_toolbar import urls as debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

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
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    path('api/v1/', include(api_patterns)),

    re_path('', include('social_django.urls', namespace='social')),
    path('auth/', auth),
    path('djdt/', include(debug_toolbar_urls)),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
