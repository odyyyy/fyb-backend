from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include, re_path

from users.views import auth

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api-auth/', include('rest_framework.urls')),
                  re_path('', include('social_django.urls', namespace='social')),
                  path('auth/', auth),
                  path('vacancies/', include('vacancies.urls')),
                  path('bands/', include('bands.urls')),
                  path('users/', include('users.urls')),
                  path('news/', include('news.urls')),
                  path('djdt/', include('debug_toolbar.urls')),
              ] + debug_toolbar_urls()


