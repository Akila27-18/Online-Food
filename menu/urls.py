from django.urls import path, include
from rest_framework_nested import routers
from .views import RestaurantViewSet, CategoryViewSet, MenuItemViewSet

# Base router
router = routers.DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'categories', CategoryViewSet)

# Nested router
restaurants_router = routers.NestedDefaultRouter(router, r'restaurants', lookup='restaurant')
restaurants_router.register(r'menu-items', MenuItemViewSet, basename='restaurant-menu-items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(restaurants_router.urls)),
]
