from django.views import View
from django.shortcuts import render
from .models import Product

class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, 'products/products_detail.html', {'products': products})
  
class MainPageView(View):
    template_name = 'products/main_page.html'

    def get(self, request, *args, **kwargs):
        # Add any additional context data you want to pass to the template
        context = {
            'some_data': 'This is some data for the template',
        }
        return render(request, self.template_name, context)
