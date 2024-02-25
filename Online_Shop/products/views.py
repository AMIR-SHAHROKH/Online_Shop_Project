from django.views import View
from django.shortcuts import render,  get_object_or_404
from .models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product , Category
from .serializers import ProductSerializer
from django.core.mail import send_mail
from django.http import HttpResponse
import requests

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

class ProductDetailAPIView(APIView):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class ProductDetailsView(View):
    def get(self, request, slug):
        # URL of your Django REST Framework API endpoint for fetching product details
        api_url = f'http://127.0.0.1:8000/api/product/{slug}?format=json'  # Update with your API endpoint URL

        try:
            print(api_url)
            # Make a GET request to fetch data from the DRF API
            response = requests.get(api_url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Extract the JSON data from the response
                data = response.json()

                # Pass the product_data to your template to display to the user
                return render(request, 'products/products_detail.html', {'product': data})
            else:
                # Handle other status codes if needed
                # For example, if the product is not found (status code 404)
                if response.status_code == 404:
                    return HttpResponse("Product not found", status=404)
                # Add more cases as needed
        except requests.exceptions.RequestException as e:
            # Handle exceptions if the request fails
            return HttpResponse("Error fetching product data", status=500)

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


def send_test_email(request):
    send_mail(
        'Test Email Subject',
        'This is a test email message.',
        'amir',
        ['nafisehmehrabi90@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse('Test email sent successfully.')
