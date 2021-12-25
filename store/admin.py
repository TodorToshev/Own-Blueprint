from django.contrib import admin
from .models import Product, Size, ProductImage

# Register your models here.

admin.site.register(Size)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    '''
    create a single Django admin from two different models. 
    With inlines, the admin can allow editing of parent and child models on one page.
    '''
    inlines = [ProductImageAdmin]
 
    #probably not needed:
    # class Meta:
    #    model = Product
