from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404,redirect
from .models import Order
from .serializers import OrderSerializer
from django.views.generic import TemplateView
from rest_framework import generics, status
from django.http import Http404
from .models import OrderItem , update_order_payment_status
from products.models import Product
from orders.models import Order,FinalAmount,Discount
from django.urls import reverse
from .serializers import OrderItemSerializer,DiscountSerializer,FinalAmountSerializer
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderDetailView(APIView):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

class FinalAmountAPIView(APIView):
    def get(self, request, order_id):
        order = Order.objects.filter(id=order_id).first()
        if not order:
            raise Http404("Order does not exist")
        
        final_amount = FinalAmount.objects.filter(order=order).first()
        if not final_amount:
            raise Http404("Final amount not found for this order")

        serializer = FinalAmountSerializer(final_amount)
        return Response(serializer.data)

class PaymentView(APIView):
    template_name = 'orders/payment_success.html'

    def get(self, request, order_id):
        return render(request, self.template_name, {'order_id': order_id })

class OrderListPageView(TemplateView):
    template_name = 'orders/order_list.html'

class AddressCheckView(TemplateView):
    template_name = 'orders/check_address.html'

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

        data = request.data
        # data = [
            # {"id": 1, "quantity": 3},
            # {"id": 3, "quantity": 1},
        # ]  # Get order items from request data

        created_order_items_data = []
        print(data)
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

            # Update the unit price based on the associated product's price and discount
            order_item.update_unit_price()

            # Calculate total amount after applying the updated unit price
            total_amount += order_item.calculate_total_price()

            # Serialize the created order item
            order_item_serializer = OrderItemSerializer(order_item)
            created_order_items_data.append(order_item_serializer.data)

        # Update total amount for the order
        order.total_amount = total_amount
        order.save()

        return Response({'message': 'Order items created successfully', 'order_items': created_order_items_data}, status=status.HTTP_201_CREATED)

class ApplyDiscountView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        final_amount_instance, created = FinalAmount.objects.get_or_create(order=order)
        final_amount = final_amount_instance.discounted_amount if final_amount_instance.discounted_amount else order.total_amount
        context = {'order': order, 'final_amount': final_amount}
        return render(request, 'orders/apply_discount.html', context)

    def post(self, request, order_id):
        action = request.POST.get('action')
        order = get_object_or_404(Order, id=order_id)
        final_amount_instance, created = FinalAmount.objects.get_or_create(order=order)

        if action == "apply_discount":
            discount_name = request.POST.get('discount_name')

            if discount_name == "No Discount":
                final_amount_instance.discounted_amount = order.total_amount
                final_amount_instance.save()
                order.discount = None  # Remove the discount if it was applied before
                order.save()
                return JsonResponse({'success': 'No discount applied.', 'final_amount': order.total_amount})

            try:
                discount = Discount.objects.get(name=discount_name)
            except Discount.DoesNotExist:
                return JsonResponse({'error': 'Discount not found.'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

            try:
                final_amount_instance.calculate_discounted_amount(discount)
                final_amount_instance.save()
                final_amount = final_amount_instance.discounted_amount
                order.discount = discount  # Set the applied discount
                order.save()
                return JsonResponse({'success': 'Discount applied successfully.', 'final_amount': final_amount})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

        elif action == "finalize_payment":
            # Mark the final amount instance as paid
            final_amount_instance.payment_status = FinalAmount.PAID
            final_amount_instance.save()
            return JsonResponse({'success': 'Payment finalized successfully.'})

        else:
            return JsonResponse({'error': 'Invalid action.'}, status=400)



            
class DiscountAPIView(generics.CreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

class CheckDiscountAPIView(APIView):
    def get(self, request):
        discount_name = request.query_params.get('discount_name')
        if not discount_name:
            return Response({'error': 'No discount name provided.'}, status=400)
        
        try:
            discount = Discount.objects.get(name=discount_name)
            serializer = DiscountSerializer(discount)
            return Response({'exists': True, 'discount_data': serializer.data})
        except Discount.DoesNotExist:
            return Response({'exists': False, 'message': 'No discount with that name.'})
