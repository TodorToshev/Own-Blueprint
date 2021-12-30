from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.main, name="store_index"),
    path('products', views.products, name="store_products"),
    path('product/<int:pk>', views.single_product, name="product"),
    path('order', views.order_view, name="order"),
]