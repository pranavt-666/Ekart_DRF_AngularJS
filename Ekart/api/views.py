from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet, ViewSet
from api import serializers
from api import models
from rest_framework import permissions, authentication
from rest_framework.response import Response
from rest_framework.decorators import action
# Create your views here.

class UserView(ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [authentication.TokenAuthentication]


class CategoryView(ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    print()
    # permission_classes = [permissions.IsAdminUser]
    # authentication_classes = [authentication.TokenAuthentication]

    @action(methods=['POST'], detail=True)
    def addproduct(self, request, *args, **kwargs):
        cat_id = kwargs.get('pk')
        print(cat_id)
        category = models.Category.objects.get(id=cat_id)
        prod_serializer = serializers.ProductSerializer(data=request.data, context={'category':category})
        if prod_serializer.is_valid():
            prod_serializer.save()
            return Response(data=prod_serializer.data)
        else:
            return Response(data=prod_serializer.errors)


    
class ProductView(ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()

    @action(methods=['GET'], detail=True)
    def add_to_cart(self, request, *args, **kwargs):
        pid = kwargs.get('pk')
        product = models.Product.objects.get(id=pid)

        cart_serializer = serializers.CartSerializer(data=request.data, context={
            'product':product,
            'user': request.user
        })
        if cart_serializer.is_valid():
            # cart_serializer.validated_data['options'] = 'in-cart'
            cart_serializer.save()
            return Response(data=cart_serializer.data)
        else:
            return Response(data=cart_serializer.errors)


class ProductReviewView(ModelViewSet):
    serializer_class = serializers.ProductReviewSerializer
    queryset = models.Review.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    @action(methods=['POST'], detail=True)
    def add_review(self, request, *args, **kwargs):
        pid = kwargs.get('pk')
        product = models.Product.objects.get(id=pid)
        user = self.request.user
        review_serializer = serializers.ProductReviewSerializer(data=request.data, 
                                                                context={
                                                                    'user':user,
                                                                    'product':product
                                                                })
        if review_serializer.is_valid():
            review_serializer.save()
            return Response(data=review_serializer.data)
        else:
            return Response(data=review_serializer.errors)