from rest_framework import serializers
from django.contrib.auth.models import User
from api import models

from rest_framework.response import Response
from rest_framework.decorators import action

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class CategorySerializer(serializers.ModelSerializer):

    is_active = serializers.BooleanField(default=True)
    class Meta:
        model = models.Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(read_only=True)
    class Meta:
        model = models.Product
        fields = '__all__'

    def create(self, validated_data):
        print('99999999',self.context.get('category'))
        category_name = self.context.get('category')
        category_id = models.Category.objects.filter(category_name=category_name)
        print(category_id)
        return models.Product.objects.create(**validated_data, 
                                             category=category_name)



class ProductReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(read_only=True)
    product_name = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    # rating = 
    class Meta:
        model = models.Review
        fields = '__all__'
        extra_kwargs = {
            'rating':{
                'required':True
            }
        }
    
    def create(self, validated_data):
        product = self.context.get('product')
        print(product)
        user = self.context.get('user')
        return models.Review.objects.create(**validated_data, 
                                            product_name=product,
                                            user=user)
    
class CartSerializer(serializers.ModelSerializer):
    choice = (('in-cart', 'in-cart'),
               ('cancelled', 'cancelled'),
               ('order-placed', 'order-placed'))
    options = serializers.ChoiceField(choices=choice,read_only=True)
    product = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    class Meta:
        model = models.Cart
        fields = '__all__'

    def create(self, validated_data):
        # print()
        product = self.context.get('product')
        user = self.context.get('user')
        print(product, user)
        return models.Cart.objects.create(**validated_data, 
                                          product=product,
                                          user=user)