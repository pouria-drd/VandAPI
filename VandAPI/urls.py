from rest_framework import routers

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from menu.api.v1.views import MenuViewSet
from panel.api.v1.views import PriceViewSet
from panel.api.v1.views import ProductViewSet
from panel.api.v1.views import CategoryViewSet

# from users.views import MyTokenObtainPairView, MyTokenRefreshView


router = routers.DefaultRouter()

router.register(r"menu", MenuViewSet, basename="menu")
router.register(r"prices", PriceViewSet, basename="price")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"categories", CategoryViewSet, basename="category")


urlpatterns = [
    path("", include(router.urls)),
    # main admin panel
    path("admin/", admin.site.urls),
    # apps
    path("api/v1/panel/", include("panel.api.v1.urls")),
    path("api/v1/menu/", include("menu.api.v1.urls")),
    # auth
    # path("api-auth/", include("rest_framework.urls")),
    # path("auth/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("auth/token/refresh/", MyTokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
