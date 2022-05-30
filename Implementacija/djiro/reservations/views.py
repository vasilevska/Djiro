from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

# Create your views here.
class DriverReservationView(APIView):
    def get(self, request):
        driverId = request.query_params.get("idD")

        if driverId:
            reservations = Reservation.objects.filter(idu=driverId)
            serializer = ReservationsSerializer(reservations, many=True)
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
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
            "status": "P",
            "idu": 1,
            "idd": 1,
            "idc": 1
        }
        """


class DjilerReservationView(APIView):
    def get(self, request):
        djilerId = request.query_params.get("idD")
        if djilerId:            
            reservations = Reservation.objects.filter(idd=djilerId)
            serializer = ReservationsSerializer(reservations, many=True)
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)
    

    
    
