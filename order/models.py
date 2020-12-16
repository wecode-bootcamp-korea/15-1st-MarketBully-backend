from django.db import models

from user.models    import User
from product.models import Product
from user.models    import Address


class Order(models.Model):
    user           = models.ForeignKey(User, on_delete=models.PROTECT)
    order_number   = models.CharField(max_length=45)
    status         = models.ForeignKey('OrderStatus', on_delete=models.PROTECT)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateField(auto_now=True)
    address        = models.ForeignKey(Address, on_delete=models.PROTECT)
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.PROTECT)

    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'order_status'

class PaymentMethod(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'payment_method'

class OftenBuying(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.SET_DEFAULT, default=1)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'often_buyings'

class Cart(models.Model):
    product  = models.ForeignKey(Product, on_delete=models.SET_DEFAULT, default=1)
    order    = models.ForeignKey(Order, on_delete=models.SET_DEFAULT, default=1)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'carts'

class Coupons(models.Model):
    name                = models.CharField(max_length=45)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    user                = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'coupons'

