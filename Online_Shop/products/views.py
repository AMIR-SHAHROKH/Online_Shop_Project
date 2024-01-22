from django.shortcuts import render
from .models import Product

def product_detail(request):
    products = Product.objects.all()
    return render(request, 'products/product_detail.html', {'product': products})

