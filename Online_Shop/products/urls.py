from django.urls import path
from . import views
from .views import *
from .views import MainPageView

app_name = "products"

urlpatterns = [
    path('api/product/<slug:slug>', views.ProductDetailAPIView.as_view(), name='product_detail_api'),
    path('product/<slug:slug>', views.ProductDetailsView.as_view(), name='product_detail'),
    path('', views.MainPageView.as_view(), name='main_page'),
    path('send-test-email/', views.send_test_email, name='send_test_email'),
]
# 'product/<int:pk>/<slug:slug>/