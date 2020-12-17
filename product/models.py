from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'categories'

class Subcategory(models.Model):
    name     = models.CharField(max_length=45)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'subcategories'

class Discount(models.Model):
    name       = models.CharField(max_length=45)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'discounts'

class DeliveryType(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'delivery_types'

class Origin(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'origins'

class PackingType(models.Model):
    packing_type      = models.CharField(max_length=45)
    cart_packing_type = models.CharField(max_length=45)

    class Meta:
        db_table = 'packing_types'

class Product(models.Model):
    name            = models.CharField(max_length=100)
    subtitle        = models.CharField(max_length=100)
    price           = models.DecimalField(max_digits=10, decimal_places=2)
    discount        = models.ForeignKey(Discount, on_delete=models.PROTECT, null=True)
    sales_unit      = models.DecimalField(max_digits=10, decimal_places=2)
    weight          = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_type   = models.ForeignKey(DeliveryType, on_delete=models.PROTECT, null=True)
    origin          = models.ForeignKey(Origin, on_delete=models.PROTECT, null=True)
    packing_type    = models.ForeignKey(PackingType, on_delete=models.PROTECT, null=True)
    allergy         = models.CharField(max_length=500)
    expiration_date = models.DateField()
    notice          = models.CharField(max_length=200, null=True)
    is_soldout      = models.BooleanField(default=False)
    image_url       = models.URLField(max_length=2000)
    subcategory     = models.ForeignKey(Subcategory, on_delete=models.PROTECT)

    class Meta:
        db_table = 'products'
