from django.urls import path

from .views import *

urlpatterns = [
    path('reservations/driver/<int:id>', DriverReservationView.as_view()),
    path('reservations/djiler/<int:id>', DjilerReservationView.as_view()),
    path('ratings/driver/<int:id>',DriverRatingsView.as_view()),
    path('ratings/djiler/<int:id>',DjilerRatingsView.as_view()),
    path('ratings/car/<int:id>',CarRatingsView.as_view()),
    path('reserved/<int:id>',HoldingsView.as_view()),
    path('rating/car/<int:id>', car_rating),
    path('rating/driver/<int:id>', driver_rating),
    path('rating/djiler/<int:id>', djiler_rating),
]
