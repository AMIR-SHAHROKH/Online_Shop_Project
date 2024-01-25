from django.contrib import admin
from .models import Order, OrderItem, Discount, FinalAmount
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Discount)