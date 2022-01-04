from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from taggit.managers import TaggableManager
from decimal import Decimal

# Create your models here.


class Size(models.Model):
    size = models.CharField(max_length=5)

    def __str__(self):
        return self.size


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.01'))])
    rating = models.FloatField(null=True, blank=True, validators=[
                               MinValueValidator(0.0), MaxValueValidator(5.0)])
    date_added = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    tags = TaggableManager()
    sizes = models.ManyToManyField(Size)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True, default='products/def.jpg')



class ProductComment(models.Model):
    name = models.CharField(max_length=250, blank=False)
    product = models.ForeignKey(
        Product, related_name='product_comments', on_delete=models.CASCADE, null=False)
    email = models.EmailField(max_length=100)
    comment = models.TextField(max_length=500)
    #validator not really necessary.
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name}"

