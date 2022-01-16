from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from taggit.managers import TaggableManager
from decimal import Decimal
from django.db.models import Avg

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

    #fixes "Pagination may yield inconsistent results with an unordered object_list..." warning.
    class Meta:
        ordering = ('id',)

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

    def get_rating(self):
        return self.product_reviews.all().aggregate(Avg('rating'))['rating__avg']


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


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country = models.CharField(max_length=750)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    paid = models.BooleanField(default=False)

    braintree_id = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"Order {self.id} by {self.first_name} {self.last_name}."

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.cartitem_set.all())



class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    #at time of creation of new cart item, the Order obj it belongs to has not been created yet, thus null=True
    items = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.DecimalField(null=True, max_digits=5, decimal_places=2)

    def get_cost(self):
        return self.product.price * self.quantity




