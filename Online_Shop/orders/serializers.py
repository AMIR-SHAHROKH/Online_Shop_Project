from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_date', 'total_amount', 'discount', 'order_items']

    # If you want to include write support for order_items, you need to override create and update methods
    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)
        return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items')
        instance.user = validated_data.get('user', instance.user)
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.save()

        # Delete existing order items
        instance.order_items.all().delete()

        # Create new order items
        for order_item_data in order_items_data:
            OrderItem.objects.create(order=instance, **order_item_data)
        return instance
