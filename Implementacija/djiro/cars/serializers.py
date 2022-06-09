from ast import Mod
from dataclasses import field
import json
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

    class Meta:
        model = Car
        depth = 2
        #fields = '__all__'
        fields = [
            "idc",
            "lat",
            "long",
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
    car_model = serializers.CharField(required=True, write_only=True)
    coordinates = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = Car
        depth = 2
        fields = [
            "coordinates",
            "year",
            "km",
            "fuel",
            "images",
            "price_per_day",
            "descr",
            "transmision",
            "type",
            "car_model",
            "manufacturer"
        ]

    def validate(self, data):

        required_fields = [
            "coordinates",
            "year",
            "km",
            "fuel",
            "images",
            "price_per_day",
            "descr",
            "transmision",
            "type",
            "car_model",
            "manufacturer"
        ]

        for req_f in required_fields:
            if req_f not in data:
                raise serializers.ValidationError(
                (f"Nema polja: {req_f}"))

        coordinates = data['coordinates']
        try:
            coordinates = json.loads(coordinates)
        except Exception:
            raise serializers.ValidationError(
                ("Parse coordinates error"))
        
        if 'lat' not in coordinates or 'long' not in coordinates:
            raise serializers.ValidationError(
                ("Nije dobar format coordinata"))

        if 'images' not in data or not data['images']:
            raise serializers.ValidationError(
                ("Nema slike"))
        return data



    def save(self, request):
        car = Car()
        user = User.objects.get(email=request.user)
        coordinates = self.validated_data.get('coordinates', '')
        coordinates = json.loads(coordinates)
        car.lat = coordinates['lat']
        car.long = coordinates['long']

        car.year = self.validated_data.get('year', '')
        car.km = self.validated_data.get('km', '')
        car.fuel = self.validated_data.get('fuel', '')
        car.price_per_day = self.validated_data.get('price_per_day', '')
        car.descr = self.validated_data.get('descr', '')
        car.transmision = self.validated_data.get('transmision', '')

        #TODO dodati car slug

        car.user = user

        car.type = self.validated_data.get('type', '')
        print(car.type)
        try:
            manufacturer = Manufacturer.objects.get(name=self.validated_data.get('manufacturer', ''))
        except ObjectDoesNotExist:
            manufacturer = Manufacturer()
            manufacturer.name = self.validated_data.get('manufacturer', '')
            manufacturer.slug = self.validated_data.get('manufacturer', '')
            manufacturer.save()
            

        try:
            model = Model.objects.get(name=request.data['car_model'], manufacturer=manufacturer)
        except ObjectDoesNotExist:
            model = Model()
            model.manufacturer = manufacturer

            model.name = request.data["car_model"]
            model.slug = f'{manufacturer.slug}-{request.data["car_model"]}'

            model.name = request.data['car_model']

            model.save()

        car.model = model

        car.images = request.FILES['images']
        car.save()

        # Now idc is created
        car.slug = f"{model.slug}-{car.idc}"
        car.save()
        return car

      
class CarUpdateSerializer(serializers.Serializer):
    coordinates = serializers.CharField(required=False, write_only=True)
    km = serializers.IntegerField(required=False, write_only=True)
    price_per_day = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, write_only=True)
    descr = serializers.CharField(required=False, write_only=True)

    def validate(self, data):
        if 'coordinates' in data:
            coordinates = data['coordinates']
            try:
                coordinates = json.loads(coordinates)
            except Exception:
                raise serializers.ValidationError(
                    ("Parse coordinates error"))
            
            if 'lat' not in coordinates or 'long' not in coordinates:
                raise serializers.ValidationError(
                    ("Nije dobar format coordinata"))
        return data
    
    def update(self, request, car):
        if 'coordinates' in request.data:
            coordinates = request.data['coordinates']
            coordinates = json.loads(coordinates)
            car.lat = coordinates['lat']
            car.long = coordinates['long']
        
        if 'km' in request.data:
            car.km = int(request.data['km'])
        
        if 'price_per_day' in request.data:
            car.price_per_day = float(request['price_per_day'])

        if 'descr' in request.data:
            car.descr = request.data['descr']
        
        car.save()



