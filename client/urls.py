from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('', index,name='dashboard'),
    path('checkout/', checkout,name='checkout'), 
    path('remove/', remove,name='remove'), 
    path('create_order/', create_order,name='create_order'),
    path('item_detail/<int:itemid>/', item_detail, name='item_detail'),
    path('validate_login/',validate_login,name='validate_login'),
    path('validate_register/',validate_register, name='validate_register'),
    path('orderpdf/',orderpdf,name='orderpdf'),
    path("order_detail/", order_detail, name='order_detail'),
    path("orderdetailspdf/", orderdetailspdf, name='orderdetailspdf'),
]
