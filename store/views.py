from decimal import Decimal
from django.db.models import Count
from django.db.models import Q
from django.db.models.expressions import F
from django.shortcuts import get_object_or_404, render, redirect
from .models import Order, Product, ProductReview, Categories, Types, Size, CartItem, Coupon
from .forms import OrderAddressForm, ReviewForm, OrderForm
from django.db.models import Avg
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.core.exceptions import EmptyResultSet
import braintree
from django.conf import settings

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)
# Create your views here.


def main(request):
    categories = Categories.objects.all()
    mens = Product.objects.filter(category=1).order_by('-date_added')[:7]
    womens = Product.objects.filter(category=2).order_by('-date_added')[:7]
    kids = Product.objects.filter(category=3).order_by('-date_added')[:7]
    return render(request, 'store/index.html', {'categories': categories, "mens": mens, "kids": kids, "womens": womens})


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

    #clear cart:
    # del request.session['cart']
    cart = request.session.get('cart')
    if not cart:
        cart = []
    for cart_id in cart:
        cart_obj = CartItem.objects.get(id=cart_id)
        
        if cart_obj.product.id == product_id:
            if cart_obj.product_size.id == size_id:
                cart_obj.quantity += quantity
                cart_obj.save()
                break
    else:
        new_cart_item = CartItem.objects.create(product=Product.objects.get(id=product_id), 
                                    product_size=Size.objects.get(id=size_id), 
                                    quantity=quantity)
        cart.append(new_cart_item.id)

    request.session['cart'] = cart
    return redirect('store:cart')


def cart_view(request):
    try:
        cart = request.session['cart']
    except Exception as e:
        return render(request, 'store/cart.html')

    context = {"cart_objects": [],}
    total_price = 0

    for item_id in cart:
        order_item = CartItem.objects.get(id=item_id)
        total_price += order_item.get_cost()
        context["cart_objects"].append(order_item)

    code = request.GET.get('code')
    if code is not None:
        coupon = Coupon.objects.get(code=code)
        # necessary to do it this way because of TypeError: 
        # unsupported operand type(s) for *: 'decimal.Decimal' and 'float'. 
        discount = round(total_price*round(Decimal(coupon.discount/100), 2),2)
        total_price -= discount
        context['coupon'] = coupon
        request.session['coupon'] = coupon.code

    context['total_price'] = total_price
        
    return render(request, 'store/cart.html', context)



def cart_remove(request, id):
    cart = request.session.get('cart')
    cart.remove(id)
    request.session['cart'] = cart
    return redirect('store:cart')


def cart_update(request, id):
    cart_item = CartItem.objects.get(id=id)
    cart_item.quantity = request.GET.get('quantity')
    cart_item.save()
    return redirect('store:cart')


def order_address(request):
    if not request.session['cart']:
        return render(request, 'store/index.html')
    form = OrderAddressForm()
    if request.method == 'POST':
        form = OrderAddressForm(request.POST)
        if form.is_valid():

            cart_items = []
            for item_id in request.session['cart']:
                order_item = CartItem.objects.get(id=item_id)
                cart_items.append(order_item)

        new_order = Order(cartitem=cart_items[0], 
                                        first_name=request.POST['first_name'],
                                        last_name = request.POST['last_name'],
                                        country = request.POST['country'],
                                        city = request.POST['city'],
                                        address = request.POST['address'],
                                        postal_code = request.POST['postal_code'])
        try:
        # if request.session['coupon']:
            new_order.coupon = Coupon.objects.get(code=request.session['coupon'])
        except KeyError:
            pass
        new_order.save()
       
        

        for cart_item in cart_items:
            new_order.cartitem_set.add(cart_item)

        request.session['order_id'] = new_order.id
        client_token = gateway.client_token.generate()
        return render(request, 'store/process.html',{"client_token":client_token, "order": new_order})

    return render(request, 'store/order_address.html', {'form': form,})




def payment_process(request):
    order_id = request.session.get('order_id')
    print(request.session.get('order_id'))
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}','payment_method_nonce': nonce, 
            'options': {'submit_for_settlement': True}})

        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            del request.session['cart']
            try:
                del request.session['coupon']
            except KeyError:
                pass
            return redirect('store:done')
        elif result.transaction:
            print("Error processing transaction:")
            print("  code: " + result.transaction.processor_response_code)
            print("  text: " + result.transaction.processor_response_text)
            del request.session['cart']
            try:
                del request.session['coupon']
            except KeyError:
                pass
            return redirect('store:done')
        else:
            for error in result.errors.deep_errors:
                print("attribute: " + error.attribute)
                print("  code: " + error.code)
                print("  message: " + error.message)
            return redirect('store:canceled')

    else:
        # generate token
        client_token = gateway.client_token.generate()
        return render(request, 'store/process.html', {'order': order, 'client_token': client_token})


def payment_done(request):
    return render(request, 'store/done.html')


def payment_canceled(request):
    return render(request, 'store/canceled.html')

