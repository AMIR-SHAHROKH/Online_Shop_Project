from django.contrib import admin
from .models import Order, OrderItem, Discount, FinalAmount
from .models import Order, OrderItem, Discount, FinalAmount

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'total_amount', 'discount')
    list_filter = ('order_date',)
    search_fields = ('id', 'user__username')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'unit_price')
    search_fields = ('id', 'order__id', 'product__name')

class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'count')
    search_fields = ('name',)

class FinalAmountAdmin(admin.ModelAdmin):
    list_display = ('order', 'discounted_amount')
    search_fields = ('order__id',)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(FinalAmount, FinalAmountAdmin)
