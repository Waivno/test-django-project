
from rest_framework import serializers
from models import Product, ProductAccess

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'owner']