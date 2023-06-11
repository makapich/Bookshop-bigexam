from rest_framework import serializers

from store.models import Book, Order, OrderItem


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'title', 'price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'user_email', 'status', 'delivery_address', 'order_id_in_shop']


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['order', 'book', 'quantity']
