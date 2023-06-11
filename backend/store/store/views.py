from rest_framework import viewsets

from store.models import Book, Order, OrderItem
from store.serializers import BookSerializer, OrderItemSerializer, OrderSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().order_by('-created_at')
    serializer_class = OrderItemSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)
