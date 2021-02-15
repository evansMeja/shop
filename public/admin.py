from django.contrib import admin
from .models import *

admin.site.register(cart)
admin.site.register(mailings)
admin.site.register(order)
admin.site.register(cartitemdetail)