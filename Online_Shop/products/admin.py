from django.contrib import admin
from .models import Category, Product, Review

class ProductInline(admin.TabularInline):
    model = Product.categories.through
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory')
    search_fields = ('name', 'subcategory')
    inlines = [ProductInline]

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'has_image', 'discount')
    list_filter = ('categories', 'price', 'discount')
    search_fields = ('name', 'description', 'categories__name', 'slug')

    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'rating', 'comment')
    list_filter = ('product', 'customer', 'rating')
    search_fields = ('product__name', 'customer__username', 'comment')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
