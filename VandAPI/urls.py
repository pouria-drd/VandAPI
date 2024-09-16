from rest_framework import routers

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from menu.v1.views import MenuViewSet
from panel.v1.views import PriceViewSet
from panel.v1.views import ProductViewSet
from panel.v1.views import CategoryViewSet


router = routers.DefaultRouter()

router.register(r"menu", MenuViewSet, basename="menu")
router.register(r"prices", PriceViewSet, basename="price")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"categories", CategoryViewSet, basename="category")


urlpatterns = [
    path("vand-api/", include(router.urls)),
    # main admin panel
    path("admin/", admin.site.urls),
    # apps
    path("vand-api/menu/v1/", include("menu.v1.urls")),
    path("vand-api/panel/v1/", include("panel.v1.urls")),
]

if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
