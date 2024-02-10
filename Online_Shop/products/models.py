from django.db import models
from django.db import models
from users.models import User
from django.db import models
from users.models import User

def upload_to(instance, filename):
    # Always return the placeholder image URL if the image is not provided
    return 'https://via.placeholder.com/300'

class Category(models.Model):
    name = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255)

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/images/', blank=True, null=True)
    description = models.TextField()
    discount = models.DecimalField(max_digits=10, decimal_places=1, blank=True ,null=True)
    price = models.IntegerField()
    categories = models.ManyToManyField(Category, related_name='products')

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
