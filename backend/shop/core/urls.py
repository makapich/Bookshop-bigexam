from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from shop.views import BookList, OrderList, Register, UserProfile, cart_add, cart_clear, cart_detail_and_create_order, \
    item_clear, item_decrement, item_increment

urlpatterns = [
    path('admin/', admin.site.urls),

    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('cart/cart_detail/', cart_detail_and_create_order, name='cart_detail'),

    path('', BookList.as_view(), name='home'),

    path("accounts/", include('django.contrib.auth.urls')),
    path("accounts/register/", Register.as_view(), name="register"),

    path("profile/<str:username>/", UserProfile.as_view(), name="profile"),

    path("my_orders/", OrderList.as_view(), name="my_orders"),

]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
