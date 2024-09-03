from shop.models import Category, Price, Product
from menu.serializers import MenuSerializer, MenuDetailSerializer

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.db.models import OuterRef, Subquery, F, BooleanField, Value, Prefetch


class MenuListView(ListAPIView):
    http_method_names = ["get"]
    serializer_class = MenuSerializer
    queryset = Category.objects.filter(is_active=True)


class MenuDetailView(RetrieveAPIView):
    lookup_field = "slug"
    http_method_names = ["get"]
    serializer_class = MenuDetailSerializer

    def get_queryset(self):
        # Subquery to fetch the most recent active price for a product
        most_recent_active_price_subquery = (
            Price.objects.filter(
                product=OuterRef("pk"),
                is_active=True,
            )
            .order_by("-created_at")
            .values("amount")[:1]
        )

        return Category.objects.prefetch_related(
            Prefetch(
                "products",
                queryset=Product.objects.filter(
                    is_active=True
                )  # Filter only active products
                .annotate(
                    most_recent_active_price=Subquery(
                        most_recent_active_price_subquery, output_field=BooleanField()
                    )
                )
                .prefetch_related("prices"),
            )
        )


class MenuViewSet(ReadOnlyModelViewSet):
    http_method_names = ["get"]
    serializer_class = MenuSerializer
    queryset = Category.objects.filter(is_active=True)
