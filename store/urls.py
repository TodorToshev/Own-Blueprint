from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.main, name="store_index"),
    path('filter', views.FilterListView.as_view(), name='filter'),
    path('products', views.ProductListView.as_view(), name="store_products"),
    path('product/<int:pk>', views.single_product, name="product"),
    path('order', views.order_view, name="order"),
]