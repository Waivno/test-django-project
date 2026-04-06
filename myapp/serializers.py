
from rest_framework import serializers
from myapp.models import Product, ProductAccess


class ProductSerializer(serializers.ModelSerializer):
    students = serializers.IntegerField(read_only=True)
    lesson_views = serializers.IntegerField(read_only=True)
    total_view_time = serializers.IntegerField(read_only=True)
    purchase_rate = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'owner', 'students', 'lesson_views', 'total_view_time', 'purchase_rate']
        read_only_fields = ['owner']