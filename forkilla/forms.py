from django import forms

from .models import Reservation
from .models import Review
from .models import Restaurant

class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ["day", "time_slot", "num_people"]

class ReviewForm(forms.ModelForm):
	
	class Meta:
		model = Review
		fields = ["restaurant_rate","comment"]

class RestaurantForm(forms.ModelForm):
	class Meta:
		model=Restaurant
		fields=['city','category','price_average']