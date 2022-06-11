from re import L
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from stripe import api_base
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import *
from .serializers import *

"""
-reservations/views.py

U ovom fajlu su napisani svi testovi za testiranje aplikacije 'reservations'

testovi se pozivaju pozivom python manage.py test reservations
U testu se pozivaju sve funkcije koje pocinju niskom test

Autori:
    -Lazar Erić
    -Stefan Branković
    -Nevena Vasilevska
    -Aleksa Račić

"""
class DriverReservationView(APIView):
    """ApiVIew for Driver reservations
    
    Atributes:
    permission_classes : tuple
        oznacava koje klase ce da hendluju autentifikaciju korisnika
    
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        """
        Autor: Stefan Branković

        funkcija koja vraca sve rezervacije korisnika
        @param request : httprequest
            get request
        @id
            id korisnika
        
        """
        driverId = id

        if driverId:
            reservations = Reservation.objects.filter(idu__pk=driverId)
            serializer = ReservationsSerializer(reservations, many=True)
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, id):
        """
        Autor: Stefan Branković

        funkcija koja dodaje novu rezervaciju yza korisnika
        @param request : httprequest
            post zahtev oblika:

            {
            "date_from": "2022-05-30",
            "date_to": "2022-06-03",
            "status": "R",
            "driver": 3,
            "djiler": 4,
            "car": 1
            }

            statusi:
            R - requested
            P - pending
            F - finished
            C - cancelled
            D - declined
        
        @id
            id korisnika
        
        """
        print(request.data)
        serializer = ReservationsSerializer(data = request.data)
        
        if serializer.is_valid():
            user_id = serializer.validated_data.get("driver")
            serializer.validated_data['idu'] = user_id
            serializer.validated_data.pop("driver")
            djiler_id = serializer.validated_data.get("djiler")
            serializer.validated_data['idd'] = djiler_id
            serializer.validated_data.pop("djiler")
            car_id = serializer.validated_data.get("car")
            serializer.validated_data['idc'] = car_id
            serializer.validated_data.pop("car")
            serializer.save()

            car = Car.objects.get(pk=car_id.idc)
            

            serializerHolding = HoldingSerializer(data = {
                "idc": serializer.validated_data['idc'].idc,
                "idr": serializer.data['idr'],
                "price": car.price_per_day,
                "date_from": serializer.validated_data['date_from'],
                "date_to": serializer.validated_data['date_to'],
            })
            if serializerHolding.is_valid():
                serializerHolding.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        """
        Autor: Stefan Branković

        funkcija koja odbija rezervaciju
        @param request : httprequest
            http put request
        @id
            id korisnika
        
        """
        try:
            res = Reservation.objects.get(idr = id)
        except:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)
        res.status = 'C'
        res.save()
        serializer = ReservationsSerializer(res)
        return Response(serializer.data)
    
class DjilerReservationView(APIView):
    """ApiVIew za rezervacije DJilera
    
    Atributes:
    permission_classes : tuple
        oznacava koje klase ce da hendluju autentifikaciju korisnika
    
    """
    
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        """
        Autor: Aleksa Račić

        funkcija koja vraca sve rezervacije djilera        @param request : httprequest
            get request
        @id
            id korisnika
        
        """
        djilerId = id
        if djilerId:            
            reservations = Reservation.objects.filter(idd__pk=djilerId)
            serializer = ReservationsSerializer(reservations, many=True)
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)

    def post(self, request, id):
        """
        Autor: Aleksa Račić

        funkcija koja dodaje novu rezervaciju yza korisnika
        @param request : httprequest
            post zahtev oblika:
            {
            "accept":1
            }
        @id
            id korisnika
        
        """
        try:
            res = Reservation.objects.get(idr = id)
        except:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)
        if 'accept' in request.data and int(request.data['accept']):
            res.status = 'P'
        else:
            res.status = 'D'
        res.save()
        serializer = ReservationsSerializer(res)
        return Response(serializer.data)

class DriverRatingsView(APIView):
    """ApiVIew za hendlovanje ocena za vozace
    
    Atributes:
    permission_classes : tuple
        oznacava koje klase ce da hendluju autentifikaciju korisnika
    
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, id):
        """
        Autor: Nevena Vasilevska

        funkcija koja vraca sve ocene vozaca       
        @param request : httprequest
            get request
        @id
            id vozaca
        
        """
        if id:            
            ratings = Ratingdriver.objects.filter(idu=id)
            serializer = DriverRatingSerializer(ratings, many=True)
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)

    def post(self, request, id):
        """
        Autor: Nevena Vasilevska

        funkcija koja dodaje ocenu vozaca       
        @param request : httprequest
            post request oblika:
            {
                "rating": 4,
                "descr": "Kida!!!",
                "idr": reservation.id,
                "idu": user.id,
                "idd": self.user_verif.id
            }
        @id
            id rezervacije
        
        """
        serializer = DriverRatingSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)


class CarRatingsView(APIView):
    """ApiVIew za hendlovanje ocena za automobile
    
    Atributes:
    permission_classes : tuple
        oznacava koje klase ce da hendluju autentifikaciju korisnika
    
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, id):
        """
        Autor: Aleksa Račić

        funkcija koja vraca sve ocene automobila       
        @param request : httprequest
            get request
        @id
            id automobila
        
        """
        if id:
            ratings = Ratingcar.objects.filter(idc=id)
            serializer = CarRatingSerializer(ratings, many=True)
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)

    def post(self, request, id):
        """
        Autor: Nevena Vasilevska

        funkcija koja dodaje ocenu automobila       
        @param request : httprequest
            post request oblika:
            {
                "car_rating": 5,
                "descr": "Odlican.",
                "djiler_rating": 3,
                "descr_djiler": "Problemi u komunikaciji",
                "idr": 1,
                "idc": 1,
                "idu": 3,
                "idd": 2
            }
        @id
            id rezervacije
        
        """
        serializer = CarRatingSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)

class DjilerRatingsView(APIView):
    """ApiVIew za hendlovanje ocena za Djilera"""

    def get(self, request, id):
        """
        Autor: Aleksa Račić

        funkcija koja vraca sve ocene Djilera       
        @param request : httprequest
            get request
        @id
            id Djilera
        
        """
        if id:            
            ratings = Ratingcar.objects.filter(idd = id)
            serializer = DjilerRatingSerializer(ratings, many=True)
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)

class HoldingsView(APIView):
    """ApiVIew za hendlovanje trenutnih holdova"""
    def get(self, request, id):
        """
        Autor: Lazar Erić

        funkcija koja vraca sve Holdings auta      
        @param request : httprequest
            get request
        @id
            id Automobila
        
        """
        holdings = Holding.objects.filter(idc = id)
        serializer = HoldingSerializer(holdings, many = True)
        return Response(serializer.data)

@api_view(['GET'])
def car_rating(request, id):
    """
    Autor: Aleksa Račić

    funkcija koja vraca prosek ocena automobila    
    @param request : httprequest
        get request
    @id
        id Automobila
    
    """
    ratings = Ratingcar.objects.filter(idc=id)
    count = 0
    sum = 0.0
    for rating in ratings:
        count+=1
        sum+=rating.car_rating
    if(count != 0):
        return Response({"rating": sum/count, "count": count})
    else:
        return Response({"rating": 0, "count": count})

    
@api_view(['GET'])
def djiler_rating(request, id):
    """
    Autor: Aleksa Račić

    funkcija koja vraca prosek ocena Djilera   
    @param request : httprequest
        get request
    @id
        id Usera
    
    """
    ratings = Ratingcar.objects.filter(idd=id)
    count = 0
    sum = 0.0
    for rating in ratings:
        count+=1
        sum+=rating.djiler_rating
    if(count != 0):
        return Response({"rating": sum/count, "count": count})
    else:
        return Response({"rating": 0, "count": count})
    
@api_view(['GET'])
def driver_rating(request, id):
    """
    Autor: Aleksa Račić

    funkcija koja vraca prosek ocena vozaca   
    @param request : httprequest
        get request
    @id
        id korisnika
    
    """
    ratings = Ratingdriver.objects.filter(idu=id)
    count = 0
    sum = 0.0
    for rating in ratings:
        count+=1
        sum+=rating.rating
    if(count != 0):
        return Response({"rating": sum/count, "count": count})
    else:
        return Response({"rating": 0, "count": count})
    
    

    
