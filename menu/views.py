from rest_framework import viewsets
from .models import Restaurant, Category, MenuItem
from .serializers import RestaurantSerializer, CategorySerializer, MenuItemSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):  # Public access
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        queryset = MenuItem.objects.all()

        # Nested filter by restaurant
        restaurant_id = self.kwargs.get("restaurant_pk")
        if restaurant_id:
            queryset = queryset.filter(restaurant_id=restaurant_id)

        # Extra filters (optional)
        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        available = self.request.query_params.get("available")
        if available in ["true", "false"]:
            queryset = queryset.filter(is_available=(available == "true"))

        return queryset
