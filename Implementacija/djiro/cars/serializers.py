from dataclasses import field
from rest_framework import serializers

from .models import *

class CarSerilizer(serializers.ModelSerializer):

    #image = serializers.SerializerMethodField('get_image')

    class Meta:
        model = Car
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
        ]