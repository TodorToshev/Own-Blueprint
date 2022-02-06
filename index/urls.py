from django.views.generic.base import TemplateView
from .views import main
from django.urls import path

app_name='index'

urlpatterns = [
    path('', main),
]