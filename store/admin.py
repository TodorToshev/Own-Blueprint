from django.contrib import admin
from .models import Coupon, Product, Size, ProductImage, ProductReview, Categories, Types, Order

# Register your models here.

admin.site.register(Size)
admin.site.register(ProductReview)
admin.site.register(Categories)
admin.site.register(Types)
admin.site.register(Order)
admin.site.register(Coupon)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    '''
    create a single Django admin from two different models. 
    With inlines, the admin can allow editing of parent and child models on one page.
    '''
    inlines = [ProductImageAdmin]
    list_display = ['name', 'price', 'date_added','rating', 'category', 'product_type']
    list_filter = ['rating', 'tags', 'sizes', 'category', 'product_type']
 
    #probably not needed:
    # class Meta:
    #    model = Product
