from django.urls import path
from . import views


urlpatterns = [
    path('', views.payment_init, name='create'),
    path('process/', views.payment_process, name='process'),
    path('success/', views.payment_success, name='success'), 
    path('canceled/', views.payment_canceled, name='canceled'),
]
