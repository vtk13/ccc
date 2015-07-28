from django.conf.urls import patterns, include, url
from django.contrib import admin

import registration.backends.default.urls
import registration.auth_urls

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('goods.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
