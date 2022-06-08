from ast import Mod
from dataclasses import field
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from users.models import User

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
            "user",
            "type",
            "slug",
            "get_image",
            "get_thumbnail",
            "get_absolute_url",
            "model",
        ]


class CarCreation(serializers.ModelSerializer):
    manufacturer = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = Car
        depth = 2
        fields = [
            "coordinates",
            "year",
            "km",
            "fuel",
            "images",
            "thumbnail",
            "price_per_day",
            "descr",
            "transmision",
            "user",
            "type",
            "model",
            "manufacturer"
        ]

    def validate(self, data):
        print(data)
        if not data['images']:
            raise serializers.ValidationError(
                ("Nema slike"))
        return data
    

    
    def save(self, request):
        car = Car()
        user = User.objects.get(email=request.user)
        car.coordinates = self.validated_data.get('coordinates', '')
        car.year = self.validated_data.get('year', '')
        car.km = self.validated_data.get('km', '')
        car.fuel = self.validated_data.get('fuel', '')
        car.price_per_day = self.validated_data.get('price_per_day', '')
        car.descr = self.validated_data.get('descr', '')
        car.transmision = self.validated_data.get('transmision', '')

        car.user = user

        car.type = self.validated_data.get('type', '')
        try:
            manufacturer = Manufacturer.objects.get(name=self.validated_data.get('manufacturer', ''))
        except ObjectDoesNotExist:
            manufacturer = Manufacturer()
            manufacturer.name = self.validated_data.get('manufacturer', '')
            manufacturer.slug = self.validated_data.get('manufacturer', '')

        
        try:
            model = Model.objects.get(name=request.data['model'], manufacturer=manufacturer)
        except ObjectDoesNotExist:
            model = Model()
            model.manufacturer = manufacturer
            model.name = request.data['model']
            model.save()
            
        car.model = model
        
        car.images = request.FILES['images']

        car.save()

        return car



