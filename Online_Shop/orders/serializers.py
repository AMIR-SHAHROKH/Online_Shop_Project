from rest_framework import serializers
from .models import Order, OrderItem,Discount,FinalAmount
from products.models import Product

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

class OrderfinalSerializer(serializers.ModelSerializer):
    discount_id = serializers.IntegerField(required=False)

    class Meta:
        model = Order
        fields = ['total_amount', 'discount_id']
        
class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'discount','image','description']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductDetailsSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_date', 'total_amount', 'discount', 'order_items','payment_status']

    # If you want to include write support for order_items, you need to override create and update methods
    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        order_items_data = OrderItemSerializer(order_items, many=True).data
        total_amount = obj.total_amount  # Assuming total_amount is a field in the Order model
        payment_status = obj.payment_status
        return {'order_items': order_items_data, 'total_amount': total_amount, 'payment_status' : payment_status}
        
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
class FinalAmountSerializer(serializers.ModelSerializer):
    # Use a read-only field to represent the order's ID
    order_id = serializers.PrimaryKeyRelatedField(source='order', read_only=True)

    class Meta:
        model = FinalAmount
        fields = ['discounted_amount', 'payment_status', 'order_id']