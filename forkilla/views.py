# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from .models import RestaurantInsertDate
from .models import Restaurant
from .models import Reservation
from .models import ViewedRestaurants
from .models import Review
from .forms import ReservationForm
from .forms import ReviewForm
from .forms import RestaurantForm
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import *
from rest_framework import generics
from rest_framework.decorators import api_view
from .permissions import *
from rest_framework import permissions

def index(request):
    return HttpResponse("Hello, world. You're at the Forkilla home page.")

def home(request):
	viewedrestaurants = _check_session(request)
	restaurants_promot = Restaurant.objects.filter(is_promot="True")
	print(request.user.is_authenticated())
	context = {
		'restaurants':restaurants_promot,
		'viewedrestaurants': viewedrestaurants
	}
	return render(request,'forkilla/home.html',context)

"""def details(request,number=""):
	restaurant = Restaurant.objects.filter(restaurant_number=number)
	context = {
		'restaurants' : restaurant
	}

	return render(request,'forkilla/details.html',context)"""

def restaurants(request,city="",category=""):
	city_search = request.GET.get('q','')
	viewedrestaurants = _check_session(request)
	if city and category:
		restaurants_by_city = Restaurant.objects.filter(city__iexact=city).filter(category=category)
	elif city:
		restaurants_by_city = Restaurant.objects.filter(city__iexact=city)
	elif city_search:
		restaurants_by_city = Restaurant.objects.filter(city__iexact=city_search)
		city = city_search
	else:
		restaurants_by_city =  Restaurant.objects.all()
	context = {
		'city': city,
		'category':category,
		'restaurants': restaurants_by_city,
		'viewedrestaurants': viewedrestaurants
	}
	return render(request, 'forkilla/restaurants.html', context)

def ple(resv):
	tot = 0
	day = resv.day
	slot = resv.time_slot
	rest = resv.restaurant
	list_res = Reservation.objects.filter(restaurant = rest, day = day, time_slot = slot)
	for res in list_res:
		tot += res.num_people

	return tot + resv.num_people > rest.capacity

@login_required
def reservation(request):
	try:
		viewedrestaurants = _check_session(request)
		if request.method == "POST":
			form = ReservationForm(request.POST)
			if form.is_valid():
				resv = form.save(commit=False)
				restaurant_number = request.session["reserved_restaurant"]
				resv.restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
				resv.user = request.user
				if(ple(resv)):
					request.session["result"] = "NOT_OK"
					#"Netejar" variables com ferho xd xd
				else:
					resv.save()
					request.session["reservation"] = resv.id
					request.session["result"] = "OK"
					#"Netejar" variables com ferho xd xd
			else:
				request.session["result"] = form.errors
				return HttpResponseRedirect(reverse('checkout'))

		elif request.method == "GET":
			restaurant_number = request.GET["reservation"]
			restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
			request.session["reserved_restaurant"] = restaurant_number

		form = ReservationForm()
		context = {
			'restaurant': restaurant,
			'viewedrestaurants': viewedrestaurants,
			'form': form
		}

	except Restaurant.DoesNotExist:
		return HttpResponse("Restaurant Does not exists")
	return render(request, 'forkilla/reservation.html', context)

def _check_session(request):

    if "viewedrestaurants" not in request.session:
        viewedrestaurants = ViewedRestaurants()
        viewedrestaurants.save()
        request.session["viewedrestaurants"] = viewedrestaurants.id_vr
    else:
        viewedrestaurants = ViewedRestaurants.objects.get(id_vr=request.session["viewedrestaurants"])
    return viewedrestaurants

def details(request,restaurant_number=""):

	viewedrestaurants = _check_session(request)
	restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
	lastviewed = RestaurantInsertDate(viewedrestaurants=viewedrestaurants,restaurant= restaurant)
	lastviewed.user = request.user
	lastviewed.save()

	foto_name = restaurant.featured_photo.url[16:]

	reviews = Review.objects.filter(restaurant = restaurant)
	context = {
		'foto_name':foto_name,
		'restaurant': restaurant,
		'viewedrestaurants': viewedrestaurants,
		'reviews':reviews
	}
	return render(request, 'forkilla/details.html', context)

def checkout(request):
	viewedrestaurants = _check_session(request)
	context = {
		'result':request.session["result"],
		'viewedrestaurants': viewedrestaurants
	}

	#"Netejar" variables com ferho xd xd

	return render(request, 'forkilla/checkout.html', context)
@login_required
def review(request,restaurant_number = ''):
	if request.method == "POST":
		form = ReviewForm(request.POST)
		if form.is_valid():
			comm = form.save(commit=False)
			restaurant_number = request.session["restaurant_number"]
			comm.restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
			comm.user = request.user
			comm.save()
			request.session["comment"] = comm.id
			return HttpResponseRedirect(reverse('restaurants'))
	if request.method == "GET":
		viewedrestaurants = _check_session(request)
		form = ReviewForm()
		request.session["restaurant_number"] = restaurant_number
	context = {
		'num':restaurant_number,
		'viewedrestaurants': viewedrestaurants,
		'form':form
	}
	return render(request, 'forkilla/review.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
    	'form': form,
    })
@login_required
def reservationlist(request):
	if request.method == 'POST':
		id_reserv= request.POST.get('rest')
		Reservation.objects.filter(id=id_reserv).delete()

	reservations_futures = Reservation.objects.filter(user=request.user).order_by('day').filter(day__range = [datetime.now().date(),"2300-01-01"])
	reservations_pasades = Reservation.objects.filter(user=request.user).order_by('-day').filter(day__range = ["1900-01-01",datetime.now().date().replace(day=datetime.now().day -1)])
	context = {
		'reservations_futures':reservations_futures,
		'reservations_pasades':reservations_pasades
	}
	return render(request,'forkilla/resvlist.html',context)

def comparator(request):
	if request.method =='POST':
		form = RestaurantForm(request.POST)
	else:
		form=RestaurantForm()
	return render(request,'forkilla/comparator.html',{'form':form})

class RestaurantViewSet(viewsets.ModelViewSet):

	queryset = Restaurant.objects.all()
	serializer_class = RestaurantSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsCommercialOrReadOnly)

	def delete():
		pass

	def get_queryset(self):
		queryset = Restaurant.objects.all()
		category = self.request.query_params.get('category',None)
		city = self.request.query_params.get('city',None)
		price_average = self.request.query_params.get('price_average',None)
		print(category)
		print(city)
		print(price_average)
		if category is not None:
			queryset = queryset.filter(category = category)
			print(len(queryset))
		if city is not None:
			queryset = queryset.filter(city = city)
			print(len(queryset))
		if price_average is not None:
			queryset = queryset.filter(price_average = price_average)

		return queryset

class ReviewsViewSet(viewsets.ModelViewSet):
	queryset = Review.objects.all().order_by('restaurant_rate')
	serializer_class = ReviewSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsCommercialOrReadOnly)
	def put(self, request, pk, format=None):
		pass

