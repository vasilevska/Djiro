from random import random
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image
from io import BytesIO
import json

import copy

from users.models import User
from cars.models import Car

from .views import CarsByDistanceList
from .serializers import *


class CarsTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            email='jacob@gmail.com', password='top_secret')
        self.client = APIClient()

    
    def login_user(self):
        # Request jwt token for created user
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def get_mock_img(self, name='test.jpeg', ext='jpeg', size=(50, 50)):
        byte_obj = BytesIO()
        image = Image.new(mode="RGB", size=size)
        image.save(byte_obj, ext)
        byte_obj.seek(0)
        return byte_obj.read()
    
    def test_create_listing_success(self):
        self.login_user()
        url = reverse('create_car')

        image = SimpleUploadedFile("photo.jpeg", self.get_mock_img(), content_type="image/jpeg")
        coords =json.dumps({
            "lat":44.815067291259766,
            "long":20.460474014282227
            })
        request = {
            'coordinates' : coords,
            'year': '2002',
            'manufacturer' : 'Peugeot',
            'car_model': '308',
            'fuel': 'Dizel',
            'price_per_day' : 403.5,
            'transmision' : 'manual',
            'descr' : 'Jako dobar auto',
            'images' : image,
            'km' : 3000,
            'type' : 'Sedan'
        }

        response = self.client.post(url, request, headers={"Content-Type": "multipart/form-data"})
        self.assertEqual(response.status_code, 201)
        
    
    def test_missing_field(self):
        self.login_user()
        url = reverse('create_car')

        image = SimpleUploadedFile("photo1.jpeg", self.get_mock_img(), content_type="image/jpeg")
        coords =json.dumps({
            "lat":44.815067291259766,
            "long":20.460474014282227
            })
        full_request = {
            'coordinates' : coords,
            'year': '2002',
            'manufacturer' : 'Peugeot',
            'car_model': '308',
            'fuel': 'Dizel',
            'price_per_day' : 403.5,
            'transmision' : 'mannual',
            'descr' : 'Jako dobar auto',
            'images' : image,
            'km' : 3000,
            'type' : 'Sedan'
        }

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

        for field in fields:
            request = copy.deepcopy(full_request)
            request.pop(field, None)
            
            response = self.client.post(url, request, headers={"Content-Type": "multipart/form-data"})
            self.assertEqual(response.status_code, 400)

    def test_bad_coords(self):
        self.login_user()
        url = reverse('create_car')

        image = SimpleUploadedFile("photo1.jpeg", self.get_mock_img(), content_type="image/jpeg")
        coords =json.dumps({
            "lat":44.815067291259766
            })
        request = {
            'coordinates' : coords,
            'year': '2002',
            'manufacturer' : 'Peugeot',
            'car_model': '308',
            'fuel': 'Dizel',
            'price_per_day' : 403.5,
            'transmision' : 'mannual',
            'descr' : 'Jako dobar auto',
            'images' : image,
            'km' : 3000,
            'type' : 'Sedan'
        }
        
        response = self.client.post(url, request, headers={"Content-Type": "multipart/form-data"})
        self.assertEqual(response.status_code, 400)

    def test_no_image(self):
        self.login_user()
        url = reverse('create_car')

        coords =json.dumps({
            "lat":44.815067291259766,
            "long":20.460474014282227
            })
        request = {
            'coordinates' : coords,
            'year': '2002',
            'manufacturer' : 'Peugeot',
            'car_model': '308',
            'fuel': 'Dizel',
            'price_per_day' : 403.5,
            'transmision' : 'mannual',
            'descr' : 'Jako dobar auto',
            'images' : '',
            'km' : 3000,
            'type' : 'Sedan'
        }
        
        response = self.client.post(url, request, headers={"Content-Type": "multipart/form-data"})
        self.assertEqual(response.status_code, 400)
        
    def test_cars_by_distance(self):
        url = reverse('cars_by_distance')

        lat = 45.0
        long = 0.6

        lat_factor = 0.4
        long_factor = 0.4

        for i in range(20):
            car = Car()
            new_lat = (2*random()-1) * lat_factor + lat
            new_long = (2*random()-1) * long_factor + long
            car.lat= new_lat
            car.long = new_long
            car.save()
        
        for i in range(20):
            car = Car()
            new_lat = lat + random() + lat_factor+0.1
            new_long = long + random() + long_factor+0.1
            car.lat= new_lat
            car.long = new_long
            car.save()

        coords=json.dumps(
            {
                'lat':lat,
                'long':long
            }
        )

        request = self.factory.get(url, {'coordinates': coords, 'long_factor':long_factor, 'lat_factor':lat_factor})
        response = CarsByDistanceList.as_view()(request)
        self.assertEqual(len(response.data), 20)
    
    def test_update_car(self):
        self.login_user()

        image = SimpleUploadedFile("photo.jpeg", self.get_mock_img(), content_type="image/jpeg")
        lat = 44.815067291259766
        long = 20.460474014282227


        year = '2002'
        manufacturer = 'Peugeot'
        car_model = '308'
        fuel = 'Dizel'
        price_per_day = 403.5
        transmision = 'manual'
        descr = 'Jako dobar auto'
        images = image
        km = 3000
        type = 'Sedan'

        car = Car()
        car.lat = lat
        car.long = long
        car.km = km
        car.price_per_day = price_per_day
        car.descr = descr
        car.slug = "123123123"

        car.save()


        new_long=27.0
        new_lat = 47.0
        coords =json.dumps({
            "lat":new_lat,
            "long":new_long
            })

        change = {
            'coordinates' : coords
        }
        id = car.idc
        url = reverse('update_car', args = [car.idc])
        response = self.client.post(url, change)

        car = Car.objects.get(pk=id)
        self.assertEqual(car.long, new_long)
        self.assertEqual(car.lat, new_lat)

        
        

