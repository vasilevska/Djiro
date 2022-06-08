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


class CreateListing(TestCase):
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
        print(response.data)
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
        