import datetime

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    categoryName = models.CharField(max_length=200)

    def __str__(self):
        return self.categoryName


class Product(models.Model):
    productName = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")
    description = models.TextField(max_length=500, blank=True, null=True)
    price = models.IntegerField()
    countInStock = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.productName


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class ShippingInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=4)
    contact = models.CharField(max_length=20)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    itemsPrice = models.IntegerField()
    shippingPrice = models.IntegerField()
    totalPrice = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    isShipped = models.BooleanField(default=False)
    shippedAt = models.DateTimeField(blank=True, null=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(blank=True, null=True)
