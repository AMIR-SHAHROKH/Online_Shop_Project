from django.test import TestCase
from .models import Order, OrderItem, Discount, FinalAmount
from users.models import User
from products.models import Product
from django.test import TestCase
from django.urls import reverse
from .models import Order, OrderItem  # Import your models
import requests
from rest_framework.test import APIClient
from rest_framework import status
class OrderModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a sample user
        cls.user = User.objects.create(username='testuser', email='test@example.com', password='testpassword')

        # Create a sample discount
        cls.discount = Discount.objects.create(name='Test Discount', percentage=10, count=5)

        # Create a sample product
        cls.product = Product.objects.create(name='Test Product', description='Test Description', price=100)

        # Create a sample order
        cls.order = Order.objects.create(user=cls.user, total_amount=1000, discount=cls.discount)

        # Create a sample order item
        cls.order_item = OrderItem.objects.create(order=cls.order, product=cls.product, quantity=2, unit_price=100)

        # Create a sample final amount
        cls.final_amount = FinalAmount.objects.create(order=cls.order, discounted_amount=900)

    def test_order_str_representation(self):
        order = Order.objects.get(id=self.order.id)
        self.assertEqual(str(order), f"Order #{order.id} - {order.user.username}")

    def test_order_item_str_representation(self):
        order_item = OrderItem.objects.get(id=self.order_item.id)
        self.assertEqual(str(order_item), f"OrderItem #{order_item.id} - {order_item.product.name}")

    def test_discount_str_representation(self):
        discount = Discount.objects.get(id=self.discount.id)
        self.assertEqual(str(discount), 'Test Discount')
    # def test_final_amount_str_representation(self):
    #     final_amount = FinalAmount.objects.get(id=self.final_amount.id)
    #     self.assertEqual(str(final_amount), f"Final Amount for Order #{final_amount.order.id}")



class OrderItemCreatorAPITest(TestCase):
    def test_order_item_creator_api(self):
        # Define the URL of the API endpoint
        api_url = reverse('order_item_creator_api')  # Update with your actual URL

        # Define the test data representing order items
        test_data = {
            "order_items": [
                {"id": 1, "quantity": 3},
                {"id": 3, "quantity": 1}
            ]
        }

        # Send a POST request to the API endpoint with the test data
        response = requests.post(api_url, json=test_data)

        # Assert that the response status code is 201 (created)
        self.assertEqual(response.status_code, 201)

        # Check if the Order object is created
        self.assertTrue(Order.objects.exists())

        # Check if the OrderItem objects are created
        self.assertTrue(OrderItem.objects.exists())

        # You can add more assertions to check specific attributes of the created objects
        # For example:
        # order = Order.objects.first()
        # order_item = OrderItem.objects.first()
        # self.assertEqual(order.user, <expected_user>)
        # self.assertEqual(order_item.order, order)
        # Add assertions based on your models and business logic
class OrderItemCreatorAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Assuming you have a user logged in
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_order_item_creation(self):
        # Define test data representing order items
        test_data = [
    {"id": 1, "quantity": 3},
    {"id": 3, "quantity": 1},
]
        # Send a POST request to the API endpoint
        url = reverse('order_item_creator_api')  # Ensure that the name matches the one defined in urls.py
        response = self.client.post(url, test_data, format='json')

        # Check if the response status code is 201 (created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if OrderItem objects are created in the database
        self.assertTrue(OrderItem.objects.exists())

