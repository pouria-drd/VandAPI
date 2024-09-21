from django.contrib import admin
from django.conf import settings
from rest_framework import routers
from django.urls import path, include
from django.conf.urls.static import static


router = routers.DefaultRouter()


base_api: str = "vand-api/"

urlpatterns = [
    path(base_api, include(router.urls)),
    # main admin
    path(base_api + "admin/", admin.site.urls),
    # api version 1
    path(base_api + "v1/menu/", include("menu.api.v1.urls")),
    path(base_api + "v1/users/", include("users.api.v1.urls")),
    path(base_api + "v1/authentication/", include("authentication.api.v1.urls")),
]

if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
