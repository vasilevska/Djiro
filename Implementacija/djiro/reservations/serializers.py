from rest_framework import serializers

from .models import *

class ReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
