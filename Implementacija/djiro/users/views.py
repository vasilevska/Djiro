from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import *
from .serializers import *

# Create your views here.
# TODO: Testing authentication through fetching users, will be returned to APIView later
class SampleView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get(self, request, format=None):
        print(request.user.id)
        users = self.get_queryset()
        serializer = UserDetailsSerializer(users, many=True)
        return Response(serializer.data)

class RetrieveIdView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    # Function to get encrypted user_id when we're logged in
    def get(self, request, format=None):
        return Response({"id": request.user.id})


class UserRegistration(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        print(request.data)
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request)
            serializer = UserDetailsSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)