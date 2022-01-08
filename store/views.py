from django.db.models import Count
from django.db.models import Q
from django.db.models.expressions import F
from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, ProductReview, Categories, Types, Size, CartItem
from .forms import ReviewForm, OrderForm
from django.db.models import Avg
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.core.exceptions import EmptyResultSet

# Create your views here.

def main(request):
    categories = Categories.objects.all()
    return render(request, 'store/index.html', {'categories': categories})


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

    def get_queryset(self):
        if self.kwargs.get('category'):
            '''if the view is accessed from url 'category/<str:category>'. It passes 
            str of men/women/kids/accessories to view. get_queryset() filters 'Category' objects 
            by 'category' capitalized variable. 'category' gets passed in lowercase. The DB 'Category' 
            models are capitalized. Either call .capitalize() on the category variable or change 
            DB models to lowercase.'''
            return Product.objects.filter(category__category=(self.kwargs.get('category')).capitalize())  
        else:
            '''if no 'category' is passed, the view is accessed from /filter url. 
            The view returns Product objects to html by generating QS from the data 
            in the GET parameters of the sidebar form in the store/products.html.'''
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

    #add cart to session w/ product id, size and quantity


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

    
    if request.method == 'POST':
        #Reviews:
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

    #Add to cart (uses GET):
    order_form = OrderForm(product)
    

            
    # paginator = Paginator(reviews, 1)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
        
    review_form = ReviewForm()
    context = {'product': product, 'order_form': order_form, 'review_form': review_form,
               'reviews': reviews, 'avg_prod_rating': avg_prod_rating, 'similar_products': similar_products}

    #update context dict w/ ratings dict.
    context.update(ratings)
    return render(request, 'store/single-product.html', context)


def order_process_view(request):
    product_id = int(request.GET.get('product'))
    size_id = int(request.GET.get('size'))
    quantity = int(request.GET.get('quantity'))

    print("Cart before append:  ", request.session['cart'])
    # del request.session['cart']
    cart = request.session.get('cart')
    if not cart:
        cart = []
        
    new_cart_item = CartItem.objects.create(product_id=Product.objects.get(id=product_id), 
                                            product_size_id=Size.objects.get(id=size_id), 
                                            quantity=quantity)

    print("New Cart Item",new_cart_item)

    if new_cart_item.id not in cart:
        cart.append(new_cart_item.id)
    # print(request.session.items())
    request.session['cart'] = cart
    print("Cart after append    ", request.session['cart'])
    
    return redirect('store:cart')


def cart_view(request):
    cart = request.session['cart']
    context = {"cart_objects": []}


    for item_id in cart:
        order_item = CartItem.objects.get(id=item_id)
        context["cart_objects"].append(order_item)

    print(context["cart_objects"]) #35
    #prod id = cart_item_objects[0].product_id  
    #prod = Product.objects.get(id=prod_id)     

    # context['order_items'] = cart_item_objects
    co = CartItem.objects.get(id=35)
    print(co)
    # p = CartItem.objects.get(product_id__id=cart_item_objects[0].id)
    # print(p)
    return render(request, 'store/cart.html', context)
