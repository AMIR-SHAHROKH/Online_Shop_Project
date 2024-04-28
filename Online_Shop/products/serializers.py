from .models import Product
from rest_framework import serializers
from .models import Product, Category

class CustomCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'subcategory')

class CustomProductSerializer(serializers.ModelSerializer):
    categories = CustomCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ( 'id', 'name', 'image', 'description', 'discount', 'price', 'categories', 'slug')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        categories_data = representation['categories']
        custom_categories_data = []
        for category_data in categories_data:
            custom_category_data = {
                'name': category_data['name'],
                'subcategory': category_data['subcategory']
            }
            custom_categories_data.append(custom_category_data)
        representation['categories'] = custom_categories_data
        return representation

