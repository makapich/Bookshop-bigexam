from django.contrib import admin

from .models import Book, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'quantity']
    list_per_page = 20
    search_fields = ['title', ]
    list_filter = ['price', 'quantity']
    list_editable = ['price', ]
    readonly_fields = ['pk', ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'status', 'created_at']
    list_filter = ['status']
    readonly_fields = ['created_at']
    inlines = [OrderItemInline, ]

    def user(self, obj):
        return obj.user.username

    user.admin_order_field = 'user__username'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity']
    list_filter = ['order']

    def book(self, obj):
        return obj.book.title

    book.admin_order_field = 'book__title'
