from django.contrib import admin
from myapp.models import Product, ProductAccess


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'created_at']
    list_filter = ['owner']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ProductAccess)
class ProductAccessAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'is_valid', 'created_at']
    list_filter = ['is_valid', 'product']
    search_fields = ['user__username', 'product__name']
    raw_id_fields = ['user', 'product']
