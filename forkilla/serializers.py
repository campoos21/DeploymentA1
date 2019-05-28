from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
        'restaurant_number', 'name', 'menu_description', 
		'price_average', 'is_promot', 'rate', 'address', 
		'city', 'country', 'featured_photo', 'category', 
		'capacity')

class ReviewSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Review
		fields = ('id','restaurant','restaurant_rate','comment')