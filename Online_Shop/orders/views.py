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
from django.core.exceptions import PermissionDenied

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
    
class OrderItemsAPIView(APIView):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id)
            serializer = OrderSerializer(order)
            order_items_data = serializer.get_order_items(order)
            return Response(order_items_data)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class OrderItemsView(TemplateView):
    template_name = 'orders/order_items.html'

    def dispatch(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        
        # Check if the order belongs to the current user
        if order.user != request.user:
            raise PermissionDenied("This order doesn't belong to you.")

        return super().dispatch(request, *args, **kwargs)
       
class OrderItemCreatorAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect the user to the accounts page for login
            return redirect(reverse('users:account'))

        data = [
   {"id": 1, "quantity": 3},
   {"id": 3, "quantity": 1},
   {"id": 2, "quantity": 2},
]  # Get order items from request data
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