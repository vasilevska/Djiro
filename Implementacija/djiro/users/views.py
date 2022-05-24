from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *

# Create your views here.


class SampleView(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
