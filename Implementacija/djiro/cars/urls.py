from django.urls import path

from .views import *

urlpatterns = [
    path('mapa/', Coords.as_view())
]
