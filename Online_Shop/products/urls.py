from django.urls import path
from . import views
from .views import *
from django.contrib.auth.decorators import login_required

app_name = "products"

urlpatterns = [
    path('api/product/<slug:slug>', views.ProductDetailAPIView.as_view(), name='product_detail_api'),
    path('product/<slug:slug>', views.ProductDetailsView.as_view(), name='product_detail'),
    path('', views.MainPageView.as_view(), name='main_page'),
    path('home/', login_required(LoggedInMainPageView.as_view()), name='logged_in_main_page'),
    path('api/products/list/', views.ProductslistAPIView.as_view() , name = 'list of products'),
    path('product/search/', views.Search.as_view(), name='search'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('categories/', views.CategoriesProductsView.as_view(), name='category-products'),
]
# 'product/<int:pk>/<slug:slug>/