from django.urls import path

from .views import *

urlpatterns = [
    path('reservations/driver/<int:id>', DriverReservationView.as_view(), name='reservations-driver'),
    path('reservations/djiler/<int:id>', DjilerReservationView.as_view(), name='reservations-djiler'),
    path('ratings/driver/<int:id>',DriverRatingsView.as_view(), name='ratings-driver'),
    path('ratings/djiler/<int:id>',DjilerRatingsView.as_view(), name='ratings-djiler'),
    path('ratings/car/<int:id>',CarRatingsView.as_view(), name='ratings-car'),
    path('reserved/<int:id>',HoldingsView.as_view(), name='reserved'),
    path('rating/car/<int:id>', car_rating, name='rating-car'),
    path('rating/driver/<int:id>', driver_rating, name='rating-driver'),
    path('rating/djiler/<int:id>', djiler_rating, name='rating-djiler'),
]
