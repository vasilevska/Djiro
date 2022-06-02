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


class RetrieveUser(generics.ListAPIView):
    serializer_class = UserDetailsSerializer

    def get_queryset(self):
        """
            Return format:
            {
                "count": 1,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "pk": 1,
                        "first_name": "",
                        "last_name": "",
                        "email": "admin@etf.rs",
                        "email_verified": null,
                        "tel": "",
                        "doc_verified": false,
                        "is_djiler": false,
                        "bio": null,
                        "get_avatar": "",
                        "get_thumbnail": "",
                        "idd": null
                    }
                ]
            }
            """
        queryset = User.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = queryset.filter(pk=id)
        return queryset



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