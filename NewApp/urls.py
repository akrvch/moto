from django.urls import path, include
from NewApp import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('shop/', views.shop_view, name='shop'),
    path('shop/search/', views.search, name='search'),
    path('add_cart/<int:pk>/<str:page>/', views.add_to_cart, name='add_to_cart'),   # str:page - страница для редиректа
    path('cart/', views.detail_cart, name='cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('delete_item/<int:pk>/', views.delete_item, name='delete_item'),
    path('shop/filter/', views.shop_filter, name='filter'),
    path('cart/order/', views.order, name='order'),
    path('cart/order/confirm/', views.new_order, name='new_order'),
    path('contacts/', views.contacts, name='contacts'),
    path('guarantee/', views.guarantee, name='guarantee'),
    path('delivery/', views.delivery, name='delivery'),
    path('oplata/', views.oplata, name='oplata'),
    path('shop/details/<int:pk>/', views.shop_detailed, name='details'),
    path('my_orders/', views.my_orders, name='my_orders'),
]