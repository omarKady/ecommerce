from django.urls import path
from .views import (
    home_page_view, about_page_view,
    feedback_page_view, search_products_view, cart_page_view,
    add_to_cart_view, delete_cart_item_view, make_order_view,
    view_customer_order
)

urlpatterns = [
    path('', home_page_view, name='home'),
    path('about/', about_page_view, name='about'),
    path('feedback/', feedback_page_view, name='feedback'),
    path('search/', search_products_view, name='search'),
    path('cart/', cart_page_view, name='cart'),
    path('add_to_cart/<int:pk>/', add_to_cart_view, name='add_to_cart'),
    path('delete_cart_item/<int:pk>/', delete_cart_item_view, name='delete_cart_item'),
    path('make_order/<int:total>', make_order_view, name='make_order'),
    path('orders/', view_customer_order, name='view_customer_order'),
]
