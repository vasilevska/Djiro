from re import L
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

# Create your views here.
class DriverReservationView(APIView):
    def get(self, request, id):
        driverId = id

        if driverId:
            reservations = Reservation.objects.filter(idu=driverId)
            serializer = ReservationsSerializer(reservations, many=True)
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, id):
        serializer = ReservationsSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)

        """
        request treba da bude:
        {
            "date_from": "2022-05-30",
            "date_to": "2022-06-03",
            "status": "R",
            "idu": 1,
            "idd": 1,
            "idc": 1
        }

        statusi:
        R - requested
        P - pending
        A - active
        C - cancelled
        D - declined
        """
    def put(self, request, id):
        try:
            res = Reservation.objects.get(idr = id)
        except:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)
        res.status = 'C'
        res.save()
        serializer = ReservationsSerializer(res)
        return Response(serializer.data)
    

    

class DjilerReservationView(APIView):
    def get(self, request, id):
        djilerId = id
        if djilerId:            
            reservations = Reservation.objects.filter(idd=djilerId)
            serializer = ReservationsSerializer(reservations, many=True)
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)

    def post(self, request, id):
        try:
            res = Reservation.objects.get(idr = id)
        except:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)
        if request.data.accept == 1 :
            res.status = 'P'
        else:
            res.status = 'D'
        res.save()
        return Response(res)


class DriverRatingsView(APIView):
    def get(self, request, id):
        if id:            
            ratings = Ratingdriver.objects.filter(idu=id)
            serializer = DriverRatingSerializer(ratings, many=True)
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)

    def post(self, request, id):
        serializer = DriverRatingSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)

    """
    {
        "rating": 4,
        "descr": "Kida!!!",
        "idr": 2,
        "idu": 2,
        "idd": 1
    }
    """

class CarRatingsView(APIView):
    def get(self, request, id):
        if id:            
            ratings = Ratingcar.objects.filter(idc=id)
            serializer = CarRatingSerializer(ratings, many=True)
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)

    def post(self, request, id):
        serializer = CarRatingSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)

class DjilerRatingsView(APIView):
    def get(self, request, id):
        if id:            
            ratings = Ratingcar.objects.filter(idd=id)
            serializer = DjilerRatingSerializer(ratings, many=True)
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)


    
    
