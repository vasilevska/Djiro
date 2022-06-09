from django.urls import path

from .views import *

urlpatterns = [
    path('list_of_all_cars/', CarsList.as_view()),
    path('car/<slug:car_slug>/', CarsDetails.as_view()),
    path('create_car/', CreateListing.as_view(), name='create_car'),
    path('get_car_by_location', CarsByDistanceList.as_view(), name='cars_by_distance'),
    path('update_car/<int:id>/', UpdateListing.as_view(), name='update_car')
]
