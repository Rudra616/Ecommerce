from django.urls import path,include
from . import views

from .views import *
urlpatterns = [
    path('', views.add_product, name='add_product'),

    path('sec/',second,name='second'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('reg/',reg,name="reg"),
    path('products/<int:id>',products,name="products"),
    path('catpro/<int:id>',catpro,name="catpro"),
    path('profile/',profile,name='profile'),
    path('checkout',checkout,name='checkout'),
    path('otp',otp,name='otp'),
    path('cartdata',cartdata,name='cartdata'),
    path('remove_item/<int:id>/',remove_item,name='remove_item')
]