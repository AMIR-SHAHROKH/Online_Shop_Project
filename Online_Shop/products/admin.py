from django.contrib import admin
from .models import Product,Category,ProductCategory,Review
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductCategory)
admin.site.register(Review)