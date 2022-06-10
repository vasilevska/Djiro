from django.urls import path

from .views import *

urlpatterns = [
    path('list_of_all_cars/', CarsList.as_view(), name='list_of_all_cars'),
    path('car/<int:idc>/', CarsDetails.as_view(), name='car'),
    path('create_car/', CreateListing.as_view(), name='create_car'),
    path('get_car_by_location', CarsByDistanceList.as_view(), name='cars_by_distance'),
    path('update_car/<slug:car_slug>/', UpdateListing.as_view(), name='update_car')
]
