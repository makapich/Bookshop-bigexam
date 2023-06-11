from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from rest_framework.authtoken import views

from store.views import BookViewSet, OrderItemViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'orderitems', OrderItemViewSet, basename='orderitem')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.ObtainAuthToken.as_view()),
    path('', include(router.urls)),
]
