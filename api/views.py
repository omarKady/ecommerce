from rest_framework import generics, permissions
from core.models import Order, Product, Feedback
from .serializers import ProductSerializer, OrderSerializer, FeedbackSerilizer, ProductDetailSerializer
# Create your views here.

class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductCreateAPI(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAdminUser]


class OrderListAPI(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OrderDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]


class FeedbackListAPI(generics.ListAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerilizer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FeedbackDetailAPI(generics.RetrieveDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerilizer
    permission_classes = [permissions.IsAdminUser]
