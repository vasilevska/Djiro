from ast import Mod
from dataclasses import field
from rest_framework import serializers

from .models import *

class ManufacturerSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Manufacturer
        fields = '__all__'

class ModelSerilizer(serializers.ModelSerializer):

    manuf = serializers.SlugRelatedField(queryset=Manufacturer.objects.all(), slug_field='slug')

    class Meta:
        model = Model
        depth = 2
        fields = '__all__'

class CarSerilizer(serializers.ModelSerializer):

    #modelP = serializers.SlugRelatedField(queryset=Model.objects.all(), slug_field='idman')

    class Meta:
        model = Car
        depth = 2
        #fields = '__all__'
        fields = [
            "idc",
            "coordinates",
            "year",
            "km",
            "fuel",
            "images",
            "thumbnail",
            "price_per_day",
            "descr",
            "transmision",
            "images",
            "type",
            "slug",
            "get_image",
            "get_thumbnail",
            "get_absolute_url",
            "model",
        ]




