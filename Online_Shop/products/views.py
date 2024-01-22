from django.shortcuts import render
from .models import Product

def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

