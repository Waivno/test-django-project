from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']


class ProductAccess(models.Model):
    product = models.ForeignKey(Product, models.PROTECT, related_name='accesses', db_index=True)
    user = models.ForeignKey(User, models.PROTECT, db_index=True)
    is_valid = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

    class Meta:
        verbose_name = 'Доступ к продукту'
        verbose_name_plural = 'Доступы к продуктам'
        unique_together = ('product', 'user')
        ordering = ['-created_at']
