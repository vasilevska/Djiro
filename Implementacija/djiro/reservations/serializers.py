from rest_framework import serializers

from .models import *

class ReservationsSerializer(serializers.ModelSerializer):
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

