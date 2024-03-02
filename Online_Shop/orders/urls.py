from django.urls import path
from .views import OrderListView, OrderDetailView, OrderListPageView, OrderDetailPageView, OrderItemCreatorAPIView,OrderItemsAPIView,OrderItemsView
from django.contrib.auth.decorators import login_required

 
app_name = "orders"

urlpatterns = [
    path('api/orders/', OrderListView.as_view(), name='order_list_api'),
    path('api/orders/<int:order_id>/', OrderDetailView.as_view(), name='order_detail_api'),
    path('', OrderListPageView.as_view(), name='order_list_page'),
    path('<int:order_id>/', OrderDetailPageView.as_view(), name='order_detail_page'),
    path('api/order-item-creator/', OrderItemCreatorAPIView.as_view(), name='order_item_creator_api'),
    path('api/order-items/<int:order_id>/', OrderItemsAPIView.as_view(), name='order-items'),
    path('order-items/<int:order_id>/', OrderItemsView.as_view(), name='order-items')
]