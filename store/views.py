from django.shortcuts import get_object_or_404, render
from .models import Product
from .forms import SizeForm

# Create your views here.

def main(request):
    return render(request, 'store/index.html')

def products(request):
    return render(request, 'store/products.html')


def single_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_sizes = product.sizes.all()
    
    size_form = SizeForm(product)

    context = {'product': product, 'sizes': product_sizes, 'size_form': size_form}
    return render(request, 'store/single-product.html', context)
