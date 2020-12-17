from django.db import models


class Order(models.Model):
    user           = models.ForeignKey("user.User", on_delete=models.PROTECT)
    order_number   = models.CharField(max_length=45)
    status         = models.ForeignKey("OrderStatus", on_delete=models.PROTECT)
    address        = models.ForeignKey("user.Address", on_delete=models.PROTECT)
    payment_method = models.ForeignKey("PaymentMethod", on_delete=models.PROTECT)
    cart           = models.ManyToManyField("product.Product", through="Cart", related_name="order_cart_set")
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateField(auto_now=True)

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


class Cart(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name="cart_order_set")
    product  = models.ForeignKey("product.Product", on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'carts'

class Coupons(models.Model):
    name                = models.CharField(max_length=45)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    user                = models.ForeignKey("user.User", on_delete=models.CASCADE)

    class Meta:
        db_table = 'coupons'

