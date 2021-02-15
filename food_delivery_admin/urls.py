from django.contrib import admin
from django.urls import path,include
from .views import *


urlpatterns = [
    path('', admin_dashboard,name='admin_dashboard'), 
    path('newitem/', newitem,name='newitem'),  
    path('manage_order/', manage_order,name='manage_order'),
    path('status/', status, name='status'),
    path('updatecallnumber',updatecallnumber,name='updatecallnumber'),
]

