from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *

from .serializers import CarSerilizer

# Create your views here.

class CarsList(APIView):
    def get(self, request, format=None):
        cars = Car.objects.all()
        serializer = CarSerilizer(cars, many=True)
        return Response(serializer.data)


class CarsDetails(APIView):
    def get_object(self, car_slug):
        try:
            return Car.objects.get(slug=car_slug)
        except Car.DoesNotExist:
            raise Http404

    def get(self, request, car_slug, format=None):
        car = self.get_object(car_slug)
        serializer = CarSerilizer(car)
        return Response(serializer.data)