from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

# Create your views here.
# TODO: Testing authentication through fetching users, will be returned to APIView later
class SampleView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get(self, request, format=None):
        users = self.get_queryset()
        serializer = UserDetailsSerializer(users, many=True)
        return Response(serializer.data)
