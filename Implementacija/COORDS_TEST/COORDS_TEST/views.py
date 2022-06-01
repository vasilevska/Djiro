from random import randint, random
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import random
import json
# Create your views here.

class Coords(APIView):
    def get(self, request, format=None):
        center={
            'lat': 45,
            'long': 45
        }
        coords = []
        for i in range(6):
            coords.append({
                'lat': 45 + (random.random()-0.5)/10,
                'long': 45 + (random.random()-0.5)/10
            })
        return Response(json.dumps({
            'center':center,
            'coords': coords
        }))  