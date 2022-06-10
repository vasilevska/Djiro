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

"""
-cars/views.py

Ovaj fajl sadrzi sve endpointe vezane za aplikaciju 'cars'

Autori:
    -Lazar Erić
    -Stefan Branković
    -Nevena Vasilevska
    -Aleksa Račić

"""

class CarsList(APIView):
    """ApiVIew for dohvatanje liste svih automobila
    """
    def get(self, request, format=None):
        """
        Autor: Stefan Branković

        funkcija koja vraca sve automobile
        @param request : httprequest
            get request
        @return listu automobila
        """
        cars = Car.objects.all()
        serializer = CarSerilizer(cars, many=True)
        return Response(serializer.data)

class CarsByDistanceList(APIView):
    """ApiVIew za dohvatanje automobila u nekom mestu
    """
    def get(self, request, format=None):
        """
        Autor: Aleksa Racic

        funkcija koja vraca sve automobile u nekom mestu
        @param request : httprequest
            get request
        @return listu automobila
        """
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
    """ApiVIew for dohvatanje informacija o automobilu
    """
    def get_object(self, idc):
        try:
            return Car.objects.get(pk=idc)
        except Car.DoesNotExist:
            raise Http404

    def get(self, request, idc, format=None):
        """
        Autor: Aleksa Račić

        funkcija koja vraca sve rezervacije djilera        
        @param request : httprequest
            get request
        @idc
            id automobila
        @return informacije o automobilu
        
        """
        car = self.get_object(idc)
        serializer = CarSerilizer(car)
        return Response(serializer.data)

class CreateListing(APIView):
    """ApiVIew for kreiranje listinga
    
    Atributes:
    permission_classes : tuple
        oznacava koje klase ce da hendluju autentifikaciju korisnika
    
    """
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        """
        Autor: Lazar Eric

        funkcija koja dodaje novi auto
        @param request : httprequest
            post zahtev sa informacijama o automobila
        
        """
        serializer = CarCreation(data=request.data)
        if serializer.is_valid():
            serializer.save(request)
            return Response({
                'message': 'Dodan novi Listing'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateListing(APIView):
    """ApiVIew for modifikovanje listinga
    
    Atributes:
    permission_classes : tuple
        oznacava koje klase ce da hendluju autentifikaciju korisnika
    
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, car_slug):
        """
        Autor: Nevena Vasilevska

        funkcija koja dodaje menja auto
        @param request : httprequest
            post zahtev sa novim informacijama o automobila
        @car_slug : slug
            slug automobila
        """
        car = Car.objects.get(slug=car_slug)
        serializer = CarUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(request, car)
            return Response({
                'message': 'Azuriran listing'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


