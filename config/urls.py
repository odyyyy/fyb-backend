from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api-auth/', include('rest_framework.urls')),
                  path('vacancies/', include('vacancies.urls')),
                  path('bands/', include('bands.urls')),
                  path('users/', include('users.urls')),
                  path('news/', include('news.urls')),
              ] + debug_toolbar_urls()
