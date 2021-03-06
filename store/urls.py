from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.main, name="store_index"),
    path('filter/', views.FilterListView.as_view(), name='filter'),
    path('products/', views.ProductListView.as_view(), name="store_products"),
    path('category/<str:category>', views.FilterListView.as_view(), name="category"),
    path('product/<int:pk>', views.single_product, name="product"),
    path('order/', views.order_process_view, name="order"),
    path('cart/', views.cart_view, name="cart"),
    path('remove/<int:id>/', views.cart_remove, name='cart_remove'),
    path('update/<int:id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.order_address, name='checkout'),
    # path('payment', views.payment_process, name='payment'),
    path('process/', views.payment_process, name='process'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
]