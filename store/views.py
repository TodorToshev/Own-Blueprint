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

    #access the form's "fields" attribute, which returns a dict: 
    #'size': <django.forms.fields.ChoiceField object...>.
    #Accessing the value, corresponding to the "size" fields
    #returns the object. Accessing the "choices" attribute returns
    #a tuple of the choices.
    choices_tuple = size_form.fields['size'].choices

    #Return a list of the individual choices.
    choices = list(map(lambda x: x[0], choices_tuple))

    context = {'product': product, 'sizes': product_sizes, 'size_form': size_form, 'choices': choices}
    return render(request, 'store/single-product.html', context)
