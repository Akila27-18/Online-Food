<<<<<<< HEAD
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.menu, name='menu'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
    path('orders/', views.order_history, name='order-history'),
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/update-order/<int:order_id>/', views.update_order, name='update-order'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
]
=======
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
>>>>>>> e15e063d4c1e5d4c2805f61d97193ed308e6a6e9
