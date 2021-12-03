from django.contrib import admin
from django.urls import path, include
# from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main),
    path('blog/', include('blog.urls', namespace='blog')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
]
