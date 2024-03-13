from django.urls import path
from .views import OrderListView, OrderDetailView, OrderListPageView, OrderDetailPageView, OrderItemCreatorAPIView,OrderItemsAPIView,OrderItemsView,ApplyDiscountView,CheckDiscountAPIView,FinalAmountAPIView,PaymentView,AddressCheckView
from django.contrib.auth.decorators import login_required

 
app_name = "orders"

urlpatterns = [
    path('api/orders/', OrderListView.as_view(), name='order_list_api'),
    path('api/orders/<int:order_id>/', OrderDetailView.as_view(), name='order_detail_api'),
    path('', OrderListPageView.as_view(), name='order_list_page'),
    path('<int:order_id>/', OrderDetailPageView.as_view(), name='order_detail_page'),
    path('api/order-item-creator/', OrderItemCreatorAPIView.as_view(), name='order_item_creator_api'),
    path('api/order-items/<int:order_id>/', OrderItemsAPIView.as_view(), name='order-items'),
    path('api/final_amount/<int:order_id>/', FinalAmountAPIView.as_view(), name='final-api'),
    path('payment/<int:order_id>/', PaymentView.as_view(), name='final-pay-status'),
    path('order-items/<int:order_id>/', OrderItemsView.as_view(), name='order-items'),
    path('apply-discount/<int:order_id>/', ApplyDiscountView.as_view(), name='apply_discount'),
    path('api/check-discount/', CheckDiscountAPIView.as_view(), name='check-discount'),
    path('address', AddressCheckView.as_view(), name='check-address')
]
