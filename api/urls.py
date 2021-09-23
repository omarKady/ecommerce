from django.urls import path, include
from .views import (
    ProductListAPI, ProductDetailAPI, OrderListAPI,
    FeedbackListAPI, FeedbackDetailAPI, OrderDetailAPI,
    ProductCreateAPI
)

urlpatterns = [
    path('', ProductListAPI.as_view()),
    path('product/<int:pk>', ProductDetailAPI.as_view()),
    path('product/create/', ProductCreateAPI.as_view()),
    path('orders/', OrderListAPI.as_view()),
    path('orders/<int:pk>', OrderDetailAPI.as_view()),
    path('feedback/', FeedbackListAPI.as_view()),
    path('feedback/<int:pk>', FeedbackDetailAPI.as_view()),
    # Add login and logout directly to the browsable api
    path('api-auth/', include('rest_framework.urls')),
]
