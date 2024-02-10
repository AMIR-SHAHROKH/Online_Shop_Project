from django.views import View
from django.shortcuts import render,  get_object_or_404
from .models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product , Category
from .serializers import ProductSerializer

class ProductList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(View):
    def get(self, request, pk, slug, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk, slug=slug)
        categories = Category.objects.all()
        return render(request, 'products/products_detail.html', {'product': product, 'categories': categories})

  
class MainPageView(View):
    template_name = 'products/main_page.html'
    def get(self, request, *args, **kwargs):
        # Add any additional context data you want to pass to the template
        products = Product.objects.all()
        categories = Category.objects.all()
        context = {
            'products': products ,'categories': categories,
        }
        return render(request, self.template_name,context)
