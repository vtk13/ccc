from django.conf.urls import patterns, include, url
from django.contrib import admin

import registration.backends.default.urls
import registration.auth_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('goods.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
]
