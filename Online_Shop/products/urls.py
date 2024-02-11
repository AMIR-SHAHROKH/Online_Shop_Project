from django.urls import path
from . import views
from .views import ProductDetailView
from .views import MainPageView

app_name = "products"

urlpatterns = [
    path('product/<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('', views.MainPageView.as_view(), name='main_page'),
    path('send-test-email/', views.send_test_email, name='send_test_email'),
]
# 'product/<int:pk>/<slug:slug>/