from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

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

class CreateListing(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        serializer = CarCreation(data=request.data)
        if serializer.is_valid():
            serializer.save(request)
            return Response({
                'message': 'Dodan novi Listing'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)