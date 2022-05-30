from django.urls import path

from .views import *

urlpatterns = [
    path('reservations/', DriverReservationView.as_view()),
]
