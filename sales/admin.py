from django.contrib import admin
from sales.models import Order, OrderItems


admin.site.register(Order)
admin.site.register(OrderItems)