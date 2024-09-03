from panel.models import Category, Price, Product
from menu.serializers import MenuSerializer, MenuDetailSerializer

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.db.models import OuterRef, Subquery, BooleanField, Prefetch


class MenuListView(ListAPIView):
    """
    API view to list all active categories.

    This view provides a read-only endpoint to retrieve a list of categories
    that are marked as active. The `MenuSerializer` is used to serialize the
    category data.
    """

    http_method_names = ["get"]
    serializer_class = MenuSerializer
    queryset = Category.objects.filter(is_active=True)


class MenuDetailView(RetrieveAPIView):
    """
    API view to retrieve details of a specific category.

    This view provides a read-only endpoint to retrieve a single category's
    details based on its slug. The `MenuDetailSerializer` is used to serialize
    the category and its related products.

    Methods:
        get_queryset: Customize the queryset to include active products and their
        most recent active prices.
    """

    lookup_field = "slug"
    http_method_names = ["get"]
    serializer_class = MenuDetailSerializer

    def get_queryset(self):
        """
        Return a queryset of active categories with prefetch related active products
        and their most recent active prices.

        This method filters for active categories and their associated active products.
        It uses a subquery to get the most recent active price for each product and
        annotates this information to the product queryset. The category queryset is
        prefetched with these annotated products to optimize database access.

        Returns:
            QuerySet: A queryset of active categories with prefetch related active products
            and their most recent active prices.
        """
        # Subquery to fetch the most recent active price for a product
        most_recent_active_price_subquery = (
            Price.objects.filter(
                product=OuterRef("pk"),
                is_active=True,  # Filter only active prices
            )
            .order_by("-created_at")
            .values("amount")[:1]
        )

        # Filter for active categories and their active products
        return Category.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                "products",
                queryset=Product.objects.filter(
                    is_active=True  # Filter only active products
                )
                .annotate(
                    most_recent_active_price=Subquery(
                        most_recent_active_price_subquery, output_field=BooleanField()
                    )
                )
                .prefetch_related("prices"),
            )
        )


class MenuViewSet(ReadOnlyModelViewSet):
    """
    ViewSet to handle read-only operations for categories.

    This viewset provides endpoints for listing and retrieving categories
    that are active. It uses the `MenuSerializer` to serialize the data.
    """

    http_method_names = ["get"]
    serializer_class = MenuSerializer
    queryset = Category.objects.filter(is_active=True)
