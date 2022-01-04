from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, ProductComment
from .forms import CommentForm, OrderForm

# Create your views here.

def main(request):
    return render(request, 'store/index.html')

def products(request):
    return render(request, 'store/products.html')


def single_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    order_form = OrderForm(product)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_review = ProductComment(name=comment_form.cleaned_data['name'], product=product, 
                          email=comment_form.cleaned_data['email'], comment=comment_form.cleaned_data['comment'], 
                          rating=int(request.POST['rating_val']))
            new_review.save()            
        else:
            print(comment_form.errors)
        
    comment_form = CommentForm()
    context = {'product': product, 'order_form': order_form, 'comment_form': comment_form}
    return render(request, 'store/single-product.html', context)


def order_view(request):
    #request.GET: QueryDict: {'quantity': ['3'], 'size': ['M']}
    return render(request, 'store/index.html')
    #TODO add if form is valid submit or sth idk. Save to db Order mdel?

