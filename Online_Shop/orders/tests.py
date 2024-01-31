from django.test import TestCase
from .models import Order, OrderItem, Discount, FinalAmount
from users.models import User
from products.models import Product

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

