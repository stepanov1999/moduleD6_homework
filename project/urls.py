from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls'), name='news'),
    path('accounts/', include('allauth.urls'), name='accounts'),
]

handler403 = 'news.views.permission_denied_view'
handler404 = 'news.views.page_not_found_view'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
