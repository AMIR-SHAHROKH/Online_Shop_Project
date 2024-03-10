from django.views import View
from rest_framework import generics
from django.shortcuts import render,  get_object_or_404, redirect
from .models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product , Category
from .serializers import CustomProductSerializer
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.generic import TemplateView
import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.core.cache import cache


class ProductList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = CustomProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CustomProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailAPIView(APIView):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        serializer = CustomProductSerializer(product)
        return Response(serializer.data)

class ProductslistAPIView(APIView):
    def get(self, request, format=None):
        # Check if data exists in cache
        cached_data = cache.get('products_data')
        if cached_data:
            return Response(cached_data)

        # Data is not cached, retrieve from the database
        products = Product.objects.all()
        serializer = CustomProductSerializer(products, many=True)
        data = serializer.data

        # Cache the data for future requests
        cache.set('products_data', data, timeout=120)  # Cache for 2 minutes

        return Response(data)



class Search(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'products/search.html')
    
    
class ProductDetailsView(View):
    def get(self, request, slug):
        # URL of your Django REST Framework API endpoint for fetching product details
        api_url = f'http://127.0.0.1:8000/api/product/{slug}?format=json'  # Update with your API endpoint URL
        product = get_object_or_404(Product, slug=slug)
        categories = product.categories.all()
        try:
            print(api_url)
            # Make a GET request to fetch data from the DRF API
            response = requests.get(api_url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Extract the JSON data from the response
                data = response.json()

                # Pass the product_data to your template to display to the user
                return render(request, 'products/products_detail.html', {'product': data, 'categories':categories})
            else:
                # Handle other status codes if needed
                # For example, if the product is not found (status code 404)
                if response.status_code == 404:
                    return HttpResponse("Product not found", status=404)
                # Add more cases as needed
        except requests.exceptions.RequestException as e:
            # Handle exceptions if the request fails
            return HttpResponse("Error fetching product data", status=500)

class LoggedInMainPageView(View):
    template_name = 'products/users_main_page.html'

    def get(self, request, *args, **kwargs):

        products = Product.objects.all()

        categories = Category.objects.all()
        context = {
            'products': products,
            'categories': categories,
        }
        return render(request, self.template_name, context)
    
class MainPageView(View):
    template_name = 'products/main_page.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('products:logged_in_main_page')
        
        products = Product.objects.all()
        categories = Category.objects.all()
        context = {
            'products': products,
            'categories': categories,
        }
        return render(request, self.template_name, context)

    
class CheckoutView(TemplateView):
    template_name = 'products/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assuming you have product data stored in a variable named 'product_list'
        product_list = [...]  # Replace [...] with your product data
        context['product_list'] = product_list
        print(product_list)
        return context
class CategoriesProductsView(APIView):
    def get(self, request):
        # Fetch all products
        products = Product.objects.all()
        
        # Serialize the products
        serializer = CustomProductSerializer(products, many=True)
        
        # Pass serialized data to the template
        return render(request, 'products/categories.html', {'products': serializer.data})
