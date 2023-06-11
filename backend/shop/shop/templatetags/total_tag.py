from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def total_price(cart):
    total = Decimal('0')
    for key, value in cart.items():
        price = Decimal(str(value['price']))
        quantity = int(value['quantity'])
        total += price * quantity
    return total

