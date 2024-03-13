from rest_framework import serializers
from .models import User, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_id', 'street', 'city', 'state', 'postal_code', 'country', 'is_shipping_address']
class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, required=False)  # Allow empty addresses

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'phone_number', 'is_active', 'addresses']

