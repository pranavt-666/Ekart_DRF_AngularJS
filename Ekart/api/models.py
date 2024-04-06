from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    product_picture = models.ImageField(upload_to='product_pic', null=True, blank=True)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.product_name


class Review(models.Model):
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=300)

    class Meta:
        unique_together = ('user', 'product_name')

    def __str__(self) -> str:
        return self.product_name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    options = (('in-cart', 'in-cart'),
               ('cancelled', 'cancelled'),
               ('order-placed', 'order-placed'))

