from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category, Product, Review
from users.models import User

class ProductModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a sample category
        cls.category = Category.objects.create(name='Test Category', subcategory='Test Subcategory')

        # Create a sample product
        cls.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            discount=10.0,
            price=100
        )

        # Create a sample user
        cls.user = User.objects.create(username='testuser', email='test@example.com')

    def test_category_creation(self):
        category = Category.objects.get(name='Test Category')
        self.assertEqual(category.subcategory, 'Test Subcategory')

    def test_product_creation(self):
        product = Product.objects.get(name='Test Product')
        self.assertEqual(product.description, 'Test Description')
        self.assertEqual(product.discount, 10.0)
        self.assertEqual(product.price, 100)

    # def test_product_category_relation(self):
    #     product_category = ProductCategory.objects.create(product=self.product, category=self.category)
    #     self.assertEqual(product_category.product, self.product)
    #     self.assertEqual(product_category.category, self.category)

    def test_review_creation(self):
        review = Review.objects.create(product=self.product, customer=self.user, rating=5, comment='Great product!')
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.customer, self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Great product!')

    # def test_image_upload(self):
    #     # Create a sample image file
    #     image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
    #     self.product.image = image_file
    #     self.product.save()

    #     # Retrieve the product and check if the image was saved correctly
    #     product = Product.objects.get(name='Test Product')
    #     self.assertTrue(product.image.name.startswith('products/images/'))  # Assuming 'products/images/' is your upload_to path