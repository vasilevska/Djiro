import json
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
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
        users = self.get_queryset()
        serializer = UserDetailsSerializer(users, many=True)
        return Response(serializer.data)


class RetrieveIdView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    # Function to get encrypted user_id when we're logged in
    def get(self, request, format=None):
        serializer = UserDetailsSerializer(request.user)
        return Response(serializer.data)


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


@permission_classes([IsAuthenticated,])
@api_view(['POST',])
def update_avatar(request, id):
    user = User.objects.get(pk=id)
    if 'avatar' in request.FILES and request.FILES['avatar'] != '':
        user.avatar = request.FILES['avatar']
        user.thumbnail = user.make_thumbnail(user.avatar)
        user.save()
        serializer = UserDetailsSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'avatar': "Failure during uploading new avatar."}, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated,])
@api_view(['POST',])
def update_user_info(request, id):
    user = User.objects.get(pk=id)
    serializer = UserUpdateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.update(user, request.data)
        user.save()
        serializer = UserDetailsSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistration(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request)
            serializer = UserDetailsSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VozackaValidation(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        serializer = DocumentDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request)
            return Response({
                'message': 'Zahtev prihvacen'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)