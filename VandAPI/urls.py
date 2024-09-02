from rest_framework import routers, viewsets

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from shop.api.v1.views import PriceViewSet
from shop.api.v1.views import ProductViewSet
from shop.api.v1.views import CategoryViewSet

# from users.views import MyTokenObtainPairView, MyTokenRefreshView


router = routers.DefaultRouter()

router.register(r"prices", PriceViewSet)
router.register(r"products", ProductViewSet)
router.register(r"categories", CategoryViewSet)

favicon_view = RedirectView.as_view(url="/static/images/favicon.ico", permanent=True)

urlpatterns = [
    path("", include(router.urls)),
    # main admin panel
    path("admin/", admin.site.urls),
    # apps
    path("api/v1/", include("shop.api.v1.urls")),
    # auth
    # path("api-auth/", include("rest_framework.urls")),
    # path("auth/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("auth/token/refresh/", MyTokenRefreshView.as_view(), name="token_refresh"),
    # protected (only for menu owners)
    # path("categories/", include("categories.urls")),
    # path("categories/<uuid:category_id>/products/", include("products.urls")),
]

if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
