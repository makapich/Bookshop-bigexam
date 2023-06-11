from django.contrib import admin

from store.models import Book, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'quantity']
    list_per_page = 20
    search_fields = ['title', ]
    list_editable = ['price', 'quantity']
    sortable_by = ['price', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user_email', 'status', 'created_at']
    list_filter = ['status']
    readonly_fields = ['created_at']
    inlines = [OrderItemInline, ]
    search_fields = ['user_email', ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity']

    def book(self, obj):
        return obj.book.title

    book.admin_order_field = 'book__title'
