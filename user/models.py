from django.db import models


class User(models.Model):
    account             = models.CharField(max_length=45)
    password            = models.CharField(max_length=2000)
    name                = models.CharField(max_length=45)
    email               = models.EmailField(max_length=254)
    phone_number        = models.CharField(max_length=45)
    gender              = models.ForeignKey('Gender', on_delete=models.PROTECT)
    birth_date          = models.DateField(null=True)
    recommender         = models.CharField(max_length=45, null=True)
    event_name          = models.CharField(max_length=100, null=True)
    grade               = models.ForeignKey('Grade', on_delete=models.PROTECT)
    terms_and_condition = models.ForeignKey('TermsAndCondition', on_delete=models.PROTECT)
    mileage             = models.DecimalField(max_digits=10, decimal_places=2)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

class Gender(models.Model):
    gender = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'genders'

class Grade(models.Model):
    grade = models.CharField(max_length=10)

    class Meta:
        db_table = 'grades'

class TermsAndCondition(models.Model):
    privacy_policy_agreement  = models.BooleanField(default=False)
    sns_marketing_agreement   = models.BooleanField(default=False)
    email_marketing_agreement = models.BooleanField(default=False)

    class Meta:
        db_table = 'terms_and_conditions'

class Address(models.Model):
    name      = models.CharField(max_length=200)
    user      = models.ForeignKey('User', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'addresses'
