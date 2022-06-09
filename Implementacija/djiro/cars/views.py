from tkinter.messagebox import YES
from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q

from .models import *
from .serializers import *

from .serializers import CarSerilizer

# Create your views here.

class CarsList(APIView):
    def get(self, request, format=None):
        cars = Car.objects.all()
        serializer = CarSerilizer(cars, many=True)
        return Response(serializer.data)

class CarsByDistanceList(APIView):
    
    def get(self, request, format=None):
        

        if 'coordinates' not in request.GET or 'long_factor' not in request.GET or 'lat_factor' not in request.GET:
            return Response({'message': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

        coordinates = request.GET['coordinates'] 

        try:
            coordinates = json.loads(coordinates)
        except Exception:
            return Response({'message': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'lat' not in coordinates or 'long' not in coordinates:
            return Response({'message': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

        lat_factor = float(request.GET['lat_factor'])
        long_factor = float(request.GET['long_factor'])

        lat = float(coordinates['lat'])
        long = float(coordinates['long'])



        cars = Car.objects.filter(
            Q(lat__lt=lat+lat_factor) & 
            Q(lat__gt = lat - lat_factor) &
            Q(long__lt = long + long_factor) &
            Q(long__gt=long - long_factor))

        
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
    
class UpdateListing(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        car = Car.objects.get(pk=id)
        serializer = CarUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(request, car)
            return Response({
                'message': 'Azuriran listing'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


