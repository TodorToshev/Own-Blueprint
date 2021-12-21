from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from taggit.managers import TaggableManager
from decimal import Decimal

# Create your models here.


class Image(models.Model):
    image = models.ImageField(upload_to='products/%Y/%m/%d')


class Size(models.Model):
    size = models.CharField(max_length=5)

    def __str__(self):
        return self.size


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    images = models.ForeignKey(
        Image, related_name='product_image', on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveIntegerField(
        null=True, blank=True, validators=[MaxValueValidator(5)])
    date_added = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    tags = TaggableManager()
    #TODO: many to many
    sizes = models.ForeignKey(Size, related_name='product_size',
                              on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
