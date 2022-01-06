from django.db.models import Count
from django.db.models import Q
from django.db.models.expressions import F
from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, ProductReview, Categories, Types, Size
from .forms import ReviewForm, OrderForm
from django.db.models import Avg
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.core.exceptions import EmptyResultSet

# Create your views here.

def main(request):
    return render(request, 'store/index.html')


class CategTypeAndSize:
    '''provides categ., type, and size to html filter sidebar via 
    'get_...()' through FilterListView and ProductListView inheritance.'''
    def get_category(self):
        return Categories.objects.all()

    def get_type(self):
        return Types.objects.all()

    def get_size(self):
        return Size.objects.all()

    
class FilterListView(CategTypeAndSize, ListView):
    '''inherits CategTypeAndSize in order to display info in filter sidebar
    on both loads of store/products.html: 1 - from loading all products via 
    ProductListView and 2 - after filtering products from this view.'''
    template_name = 'store/products.html'
    context_object_name = 'products'
    paginate_by = 9

    '''returns Product objects to html by generating QS from the data 
    in the GET parameters of the sidebar form in the store/products.html.'''
    def get_queryset(self):
        try:
            qs = Product.objects.filter(
                Q(category__in=self.request.GET.getlist('category')) & 
                Q(product_type__in=self.request.GET.getlist('type')) &
                Q(sizes__in=self.request.GET.getlist('size'))   
                )
            return qs
        except EmptyResultSet:
            pass


class ProductListView(CategTypeAndSize, ListView):
    '''inherits CategTypeAndSize in order to display info in filter sidebar
    on both loads of store/products.html: 1 - from loading all products from this view
    and 2 - after filtering products via FilterListView.'''
    model = Product
    template_name = 'store/products.html'
    context_object_name = 'products'
    paginate_by = 9


def single_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    #returns {'rating__avg': 3.6666666666666665} f. eg.
    avg_prod_rating = product.product_reviews.all().aggregate(Avg('rating'))['rating__avg']

    # uses .count() instead of len() - faster in DB! len() will retrieve a QS w/ the objects;
    # count() will perform an SQL COUNT and will not load the objects into memory to count them.
    five_star = product.product_reviews.filter(rating=5).count()
    four_star = product.product_reviews.filter(rating=4).count()
    three_star = product.product_reviews.filter(rating=3).count()
    two_star = product.product_reviews.filter(rating=2).count()
    one_star = product.product_reviews.filter(rating=1).count()
    ratings = {'os': one_star, 'ts': two_star, 'trs': three_star, 'fs': four_star, 'fvs': five_star}

    #similar products:
    product_tags_ids = product.tags.values_list('id', flat=True)
    similar_products = Product.objects.filter(tags__in=product_tags_ids).exclude(id=product.id)
    similar_products = similar_products.annotate(same_tags=Count('tags')).order_by('-same_tags',)
    #end

    reviews = product.product_reviews.all()

    order_form = OrderForm(product)
    
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            # directly create product instance from data from 
            # store.forms.ReviewForm AND! the raw HTML rating_val star inputs.
            new_review = ProductReview(name=review_form.cleaned_data['name'], product=product, 
                          email=review_form.cleaned_data['email'], comment=review_form.cleaned_data['comment'], 
                          rating=int(request.POST['rating_val']))
            new_review.save()

            #redirect to the same page to avoid form resubmission on reload.
            return redirect(product.get_absolute_url())
            
    # paginator = Paginator(reviews, 1)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
        
    review_form = ReviewForm()
    context = {'product': product, 'order_form': order_form, 'review_form': review_form,
               'reviews': reviews, 'avg_prod_rating': avg_prod_rating, 'similar_products': similar_products}

    #update context dict w/ ratings dict.
    context.update(ratings)
    return render(request, 'store/single-product.html', context)


def order_view(request):
    #request.GET: QueryDict: {'quantity': ['3'], 'size': ['M']}
    return render(request, 'store/index.html')
    #TODO add if form is valid submit or sth idk. Save to db Order mdel?

