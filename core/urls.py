from django.urls import path
from .views import ( 
    home_page_view, about_page_view,
    feedback_page_view, search_products_view, cart_page_view, 
    add_to_cart_view, delete_cart_item_view,
    recalculate_total_price_view, make_order_view
)

urlpatterns = [
    path('', home_page_view, name='home'),
    path('about/', about_page_view, name='about'),
    path('feedback/', feedback_page_view, name='feedback'),
    path('search/', search_products_view, name='search'),
    path('cart/', cart_page_view, name='cart'),
    path('add_to_cart/<int:pk>/', add_to_cart_view, name='add_to_cart'),
    path('delete_cart_item/<int:pk>/', delete_cart_item_view, name='delete_cart_item'),
    path('recalculate_total_price/', recalculate_total_price_view, name='recalculate_total_price'),
    path('make_order/<int:total>', make_order_view, name='make_order'),
]
