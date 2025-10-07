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
