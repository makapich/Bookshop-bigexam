from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    id_in_store = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS_CHOICES = (
        ('in_work', 'In Work'),
        ('success', 'Success'),
        ('fail', 'Fail'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='in_work')
    delivery_address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Order #{self.order.pk} - Item: {self.book.title}"
