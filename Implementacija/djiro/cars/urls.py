from django.urls import path

from .views import *

urlpatterns = [
    path('list_of_all_cars/', CarsList.as_view()),
    path('car/<slug:car_slug>/', CarsDetails.as_view()),
]
