from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, ProductReview
from .forms import ReviewForm, OrderForm
from django.db.models import Avg
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic.list import ListView

# Create your views here.

def main(request):
    return render(request, 'store/index.html')

class ProductListView(ListView):
    model = Product
    template_name = 'store/products.html'
    context_object_name = 'products'
    paginate_by = 9


def single_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    avg_prod_rating = product.product_reviews.all().aggregate(Avg('rating'))['rating__avg']

    #change len to .count() - faster in DB!
    five_star = len(product.product_reviews.filter(rating=5))
    four_star = len(product.product_reviews.filter(rating=4))
    three_star = len(product.product_reviews.filter(rating=3))
    two_star = len(product.product_reviews.filter(rating=2))
    one_star = len(product.product_reviews.filter(rating=1))
    ratings = {'os': one_star, 'ts': two_star, 'trs': three_star, 'fs': four_star, 'fvs': five_star}

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
            
    # paginator = Paginator(reviews, 1)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

        
    review_form = ReviewForm()
    context = {'product': product, 'order_form': order_form, 'review_form': review_form, 'reviews': reviews, 'avg_prod_rating': avg_prod_rating, }
    context.update(ratings)
    return render(request, 'store/single-product.html', context)


def order_view(request):
    #request.GET: QueryDict: {'quantity': ['3'], 'size': ['M']}
    return render(request, 'store/index.html')
    #TODO add if form is valid submit or sth idk. Save to db Order mdel?

