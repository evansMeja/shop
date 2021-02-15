from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('register', register, name='register'),
    path('login', Login, name='login'),
    path('addcart', addon, name='addcart'),
    path('savemail/',savemail, name='savemail'),
    path('search/',search, name='search'),
    path('faq',faq, name='faq'),
]

