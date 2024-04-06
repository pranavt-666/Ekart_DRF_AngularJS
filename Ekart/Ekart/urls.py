"""
URL configuration for Ekart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import UserView, CategoryView, ProductView,ProductReviewView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as authviews


router = DefaultRouter()
router.register('user', UserView, basename='user')
router.register('categories', CategoryView, basename='categories')
router.register('products' ,ProductView, basename='products')
router.register('reviews', ProductReviewView, basename='reviews' )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', authviews.obtain_auth_token)
]+router.urls
