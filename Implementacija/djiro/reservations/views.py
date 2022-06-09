from re import L
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from stripe import api_base

from .models import *
from .serializers import *

# Create your views here.
class DriverReservationView(APIView):
    def get(self, request, id):
        driverId = id

        if driverId:
            reservations = Reservation.objects.filter(idu__id=driverId)
            serializer = ReservationsSerializer(reservations, many=True)
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, id):
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
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)

        """
        request treba da bude:
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
            reservations = Reservation.objects.filter(idd__pk=djilerId)
            serializer = ReservationsSerializer(reservations, many=True)
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)

    def post(self, request, id):
        try:
            res = Reservation.objects.get(idr = id)
        except:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)
        if request.data['accept']:
            res.status = 'P'
        else:
            res.status = 'D'
        res.save()
        serializer = ReservationsSerializer(res)
        return Response(serializer.data)
        """
        {
            "accept":1
        }

        """

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
            ratings = Ratingcar.objects.filter(idd = id)
            serializer = DjilerRatingSerializer(ratings, many=True)
            return Response(serializer.data)
        else:
            return Response(data="object not found", status = status.HTTP_400_BAD_REQUEST)

class HoldingsView(APIView):
    def get(self, request, id):
        holdings = Holding.objects.filter(idc = id)
        serializer = HoldingSerializer(holdings, many = True)
        return Response(serializer.data)

@api_view(['GET'])
def car_rating(request, id):
    ratings = Ratingcar.objects.filter(idc=id)
    count = 0
    sum = 0.0
    for rating in ratings:
        count+=1
        sum+=rating.car_rating
    return Response({"rating": sum/count})
    
@api_view(['GET'])
def djiler_rating(request, id):
    ratings = Ratingcar.objects.filter(idd=id)
    count = 0
    sum = 0.0
    for rating in ratings:
        count+=1
        sum+=rating.djiler_rating
    return Response({"rating": sum/count})
    
@api_view(['GET'])
def driver_rating(request, id):
    ratings = Ratingdriver.objects.filter(idu=id)
    count = 0
    sum = 0.0
    for rating in ratings:
        count+=1
        sum+=rating.rating
    return Response({"rating": sum/count})
    
    

    
