from django.views import View
from django.shortcuts import render
from .models import Product

class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, 'products/products_detail.html', {'product': products})


