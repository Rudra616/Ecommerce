from django.urls import path,include
from . import views

from .views import *
urlpatterns = [
    path('add_product', views.add_product, name='add_product'),
    path('',second,name='second'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('reg/',reg,name="reg"),
    path('products/<int:id>',products,name="products"),
    path('catpro/<int:id>',catpro,name="catpro"),
    path('profile/',profile,name='profile'),
    path('checkout',checkout,name='checkout'),
    path('otp',otp,name='otp'),
    path('cartdata',cartdata,name='cartdata'),
    path('remove_item/<int:id>/',remove_item,name='remove_item'),
    path('order_history',order_history,name='order_history'),
    path('search/', product_search, name='product_search'),
    path('product_list/', product_list, name='product_list'),
    path('paypal',include("paypal.standard.ipn.urls")),
    path('payment_failed/', payment_failed, name='payment_failed'),
    path('payment_success/', payment_success, name='payment_success'),
    path('debug/', debug_request, name='debug_request'),
    path("create-superuser/", create_superuser),
    path("run-migrations/", run_migrations),  # New route
    path("check-session/", check_session),

]