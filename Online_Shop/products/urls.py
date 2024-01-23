from django.urls import path
from . import views
from .views import ProductDetailView

app_name = "products"

urlpatterns = [
    path('', views.ProductDetailView.as_view() , name='product_detail'),
]
