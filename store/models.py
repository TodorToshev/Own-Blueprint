from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from taggit.managers import TaggableManager
from decimal import Decimal

# Create your models here.


class Size(models.Model):
    size = models.CharField(max_length=10)

    def __str__(self):
        return self.size


class Types(models.Model):
    clothing_type = models.CharField(max_length=120)

    class Meta:
        verbose_name_plural = 'Types'

    def __str__(self):
        return self.clothing_type


class Categories(models.Model):
    category = models.CharField(max_length=80)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category

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
    category = models.ForeignKey(Categories, related_name="product_category", on_delete=models.SET_NULL, null=True, blank=True)
    product_type = models.ForeignKey(Types, related_name="product_type", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/store/product/{self.id}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="product_images", default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True, default='products/def.jpg')



class ProductReview(models.Model):
    name = models.CharField(max_length=250, blank=False)
    product = models.ForeignKey(
        Product, related_name='product_reviews', on_delete=models.CASCADE, null=False)
    email = models.EmailField(max_length=100)
    comment = models.TextField(max_length=500)
    #validator not really necessary.
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name}"

