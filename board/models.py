from django.db import models

from user.models    import User
from product.models import Product


class Review(models.Model):
    author           = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product          = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    title            = models.CharField(max_length=200)
    contents         = models.TextField()
    help_count       = models.IntegerField()
    hit_count        = models.IntegerField()
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateField(auto_now=True)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'reviews'

class Question(models.Model):
    author      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product     = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    title       = models.CharField(max_length=200)
    contents    = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateField(auto_now=True)
    is_private  = models.BooleanField(default=False)

    class Meta:
        db_table = 'questions'

class QuestionComment(models.Model):
    title      = models.CharField(max_length=200)
    contents   = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    question   = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'question_comments'

