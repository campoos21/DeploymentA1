from django.conf.urls import url

from . import views
listOfAddresses = ["161.116.56.65","161.116.56.165"]
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^restaurants/$', views.restaurants, name='restaurants'),
    url(r'^restaurants/(?P<city>.*)/$', views.restaurants, name='restaurants'),
    url(r'^restaurant/(?P<restaurant_number>.*)/$', views.details, name='detail'),
    url(r'^restaurants/(?P<city>.*)/(?P<category>.*)$', views.restaurants, name='restaurant'),
    url(r'^reservation/$', views.reservation, name='reservation'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^review/(?P<restaurant_number>.*)/$', views.review, name='review'),
    url(r'^register/$', views.register, name='register'),
    url(r'^reservas/$', views.reservationlist,name='reservationlist'),
    url(r'^comparator$', views.comparator)
]