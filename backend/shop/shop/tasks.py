import os
from decimal import Decimal

from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail as django_send_mail

from dotenv import load_dotenv

import requests

from .models import Book, Order


load_dotenv()


@shared_task
def send_mail(subject, message, from_email, to_email):
    django_send_mail(subject, message, from_email, to_email)


@shared_task
def books_sync():
    r = requests.get('http://store:8001/books/')
    books_data = r.json()

    book_ids_in_data = [book_data['id'] for book_data in books_data]

    books_in_db = Book.objects.exclude(id_in_store__in=book_ids_in_data)
    books_in_db.delete()

    for book_data in books_data:
        book, _ = Book.objects.update_or_create(
            id_in_store=book_data['id'],
            defaults={
                'title': book_data['title'],
                'price': Decimal(book_data['price']),
                'quantity': int(book_data['quantity'])
            }
        )


@shared_task
def orders_sync():
    r = requests.get('http://store:8001/orders/')
    orders_data = r.json()

    for order_data in orders_data:
        order = Order.objects.get(id=order_data['order_id_in_shop'])

        if order.status != order_data['status']:
            subject = 'Your order status was changed!'
            message = 'Check the status of your orders in "My orders" tab.'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [order.user.email, ]
            send_mail.delay(subject, message, from_email, to_email)

        order, _ = Order.objects.update_or_create(
            id=order_data['order_id_in_shop'],
            defaults={'status': order_data['status']}
        )


@shared_task
def create_order_in_api(data):
    headers = {
        'Authorization': f'Token {os.getenv("TOKEN")}',
        'Content-Type': 'application/json'
    }

    order_json = {
        'user_email': data['user_email'],
        'delivery_address': data['delivery_address'],
        'order_id_in_shop': data['order_id_in_shop']
    }

    order_post = requests.post('http://store:8001/orders/', headers=headers, json=order_json)

    order_items_json = [{'order': order_post.json()["id"], 'book': k, 'quantity': v}
                        for k, v in data['order_items'].items()]

    order_items_post = requests.post('http://store:8001/orderitems/', headers=headers, json=order_items_json)  # noqa

    subject = 'You have successfully created an order!'
    message = f'''Here are your order details:\nItems:\n{', '.join(f"{Book.objects.get(id_in_store=k).title}: {v}" for k, v in data['order_items'].items())}\nDelivery address: {data['delivery_address']}'''  # noqa
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [data['user_email'], ]
    send_mail.delay(subject, message, from_email, to_email)
