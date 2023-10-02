from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, models.PROTECT)


class ProductAccess(models.Model):
    product = models.ForeignKey(Product, models.PROTECT, related_name='accesses')
    user = models.ForeignKey(User, models.PROTECT)
    is_valid = models.BooleanField(default=True)
