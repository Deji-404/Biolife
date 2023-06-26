from django.urls import path
from .views import home_page, product_detail, add_to_cart, remove_from_cart, cart_page, register
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home_page, name='home'),
    path('product/<int:pk>', product_detail, name='product'),
    path('cart', cart_page, name='cart'),
    path('add-to-cart/<int:pk>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:pk>', remove_from_cart, name='remove-from-cart')
]

urlpatterns += [
    path('register/', register, name='register')
]

urlpatterns += [] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)