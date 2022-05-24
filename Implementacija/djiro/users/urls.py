from django.urls import path

from .views import *

urlpatterns = [
    path('nekipath/', SampleView.as_view()),
]
