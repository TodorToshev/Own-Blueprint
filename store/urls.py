from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.main, name="store"),
    path('products', views.main2, name="store2"),
]