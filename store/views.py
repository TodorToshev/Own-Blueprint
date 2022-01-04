from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, ProductReview
from .forms import ReviewForm, OrderForm

# Create your views here.

def main(request):
    return render(request, 'store/index.html')

def products(request):
    return render(request, 'store/products.html')


def single_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.product_reviews.all()

    order_form = OrderForm(product)
    
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = ProductReview(name=review_form.cleaned_data['name'], product=product, 
                          email=review_form.cleaned_data['email'], comment=review_form.cleaned_data['comment'], 
                          rating=int(request.POST['rating_val']))
            new_review.save()
            return redirect(product.get_absolute_url())
        else:
            print(review_form.errors)
        
    review_form = ReviewForm()
    context = {'product': product, 'order_form': order_form, 'review_form': review_form, 'reviews': reviews,}
    return render(request, 'store/single-product.html', context)


def order_view(request):
    #request.GET: QueryDict: {'quantity': ['3'], 'size': ['M']}
    return render(request, 'store/index.html')
    #TODO add if form is valid submit or sth idk. Save to db Order mdel?

