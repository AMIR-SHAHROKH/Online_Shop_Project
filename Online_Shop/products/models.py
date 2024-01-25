from django.db import models
from django.db import models
from users.models import User

def upload_to(instance, filename):
    # Always return the placeholder image URL if the image is not provided
    return 'https://via.placeholder.com/300'
class Category(models.Model):
    name = models.CharField(max_length=255)

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='upload_to()',blank=True, null=True)
    description = models.TextField()
    discount = models.DecimalField(max_digits=10, decimal_places=1)
    price = models.IntegerField()
    categories = models.ManyToManyField(Category, through='ProductCategory')

class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()


