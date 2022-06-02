from rest_framework import serializers

from .models import *
from users.serializers import UserDetailsSerializer

class ReservationsSerializer(serializers.ModelSerializer):
    driver = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='id', write_only=True)
    djiler = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='id', write_only=True)
    car = serializers.SlugRelatedField(queryset=Car.objects.all(), slug_field='idc', write_only=True)
    idu =  UserDetailsSerializer(read_only=True)
    idd =  UserDetailsSerializer(read_only=True)
    class Meta:
        model = Reservation
        fields = "__all__"

class DriverRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratingdriver
        fields = "__all__"

class CarRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratingcar
        fields = "__all__"

class DjilerRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratingcar
        fields = "__all__"

class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holding
        write_only_fields = ('idr','idc', 'price')
        fields = "__all__"
        extra_kwargs = {
            'idr': {'write_only': True},
            'idc': {'write_only': True},
            'price': {'write_only': True},
        }

