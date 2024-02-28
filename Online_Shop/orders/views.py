from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404,redirect
from .models import Order
from .serializers import OrderSerializer
from django.views.generic import TemplateView
from rest_framework import status
from .models import OrderItem
from products.models import Product
from orders.models import Order
from django.urls import reverse
from .serializers import OrderItemSerializer

class OrderListView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderDetailView(APIView):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

class OrderListPageView(TemplateView):
    template_name = 'orders/order_list.html'

class OrderDetailPageView(TemplateView):
    template_name = 'orders/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_id'] = kwargs['order_id']
        return context
    
test_data = [
    {"id": 1, "quantity": 3},
    {"id": 3, "quantity": 1},
]
class OrderItemCreatorAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect the user to the accounts page for login
            return redirect(reverse('users:account'))

        data =  [
    {"id": 1, "quantity": 3},
    {"id": 3, "quantity": 1},
] # Get order items from request data
        created_order_items = []
        total_amount = 0

        order = Order.objects.create(user=request.user)

        for item_data in data:
            product_id = item_data.get('id')
            quantity = item_data.get('quantity')

            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                return Response({'error': f'Product with id {product_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            # Create OrderItem instance and calculate total amount
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.price
            )
            total_amount += order_item.unit_price * order_item.quantity
            created_order_items.append(order_item)

        # Update total amount for the order
        order.total_amount = total_amount
        order.save()

        # Serialize the created order items
        serializer = OrderItemSerializer(created_order_items, many=True)

        return Response({'created_order_items': serializer.data, 'order_id': order.id}, status=status.HTTP_201_CREATED)