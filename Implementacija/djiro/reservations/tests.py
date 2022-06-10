from random import random
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image
from io import BytesIO
import json
import datetime

from .views import *
from .models import *
from users.models import *
from cars.models import Car

# Create your tests here.
class ReservationsTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            email='jacob@gmail.com', password='top_secret')
        self.user_verif = User.objects.create(
            email='jeste@gmail.com', password='top_secret', doc_verified=True)
        self.client = APIClient()
    
    def login_user(self, user):
        # Request jwt token for created user
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def get_mock_img(self, name='test.jpeg', ext='jpeg', size=(50, 50)):
        byte_obj = BytesIO()
        image = Image.new(mode="RGB", size=size)
        image.save(byte_obj, ext)
        byte_obj.seek(0)
        return byte_obj.read()

    def test_driver_reservation(self):
        self.login_user(self.user_verif)
        car = Car.objects.create(user=self.user)
        url = reverse('reservations-driver', args=[self.user_verif.id])
        response_post = self.client.post(url, 
            {
                "date_from": "2022-05-30",
                "date_to": "2022-06-03",
                "status": "R",
                "driver": self.user_verif.id,
                "djiler": self.user.id,
                "car": car.idc
            }
        )
        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(Reservation.objects.count(), 1)

        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)


        idr = response_get.data[0]['idr']
        url = reverse('reservations-driver', args=[idr])
        response_put = self.client.put(url)
        count = Reservation.objects.all().filter(status='C').count()        
        self.assertEqual(response_put.status_code, 200)
        self.assertEqual(count, 1)

    def test_djiler_reservation(self):
        self.login_user(self.user_verif)
        car = Car.objects.create(user=self.user)
        url = reverse('reservations-driver', args=[self.user_verif.id])
        response_post = self.client.post(url, 
            {
                "date_from": "2022-05-30",
                "date_to": "2022-06-03",
                "status": "R",
                "driver": self.user_verif.id,
                "djiler": self.user.id,
                "car": car.idc
            }
        )

        self.login_user(self.user)
        url = reverse('reservations-djiler', args=[self.user.id])
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_get.data[0]['idc'], car.idc)

        idr = response_get.data[0]['idr']
        url = reverse('reservations-djiler', args=[idr])
        response_accept = self.client.post(url, {"accept": 1})
        count = Reservation.objects.all().filter(status='P').count()   
        self.assertEqual(response_accept.status_code, 200)
        self.assertEqual(count, 1)

        response_decline= self.client.post(url, {"accept": 0})
        count = Reservation.objects.all().filter(status='D').count()
        self.assertEqual(response_decline.status_code, 200)
        self.assertEqual(count, 1)

    def test_driver_ratings(self):
        self.login_user(self.user_verif)
        car = Car.objects.create(user=self.user)
        url = reverse('reservations-driver', args=[self.user_verif.id])
        response_post = self.client.post(url, 
            {
                "date_from": "2022-05-30",
                "date_to": "2022-06-03",
                "status": "R",
                "driver": self.user_verif.id,
                "djiler": self.user.id,
                "car": car.idc
            }
        )
        
        self.login_user(self.user)
        url = reverse('ratings-driver', args=[self.user_verif.id])
        response_post = self.client.post(url,
            {
                "rating": 4,
                "descr": "Kida!!!",
                "idr": response_post.data['idr'],
                "idu": self.user_verif.id,
                "idd": self.user.id
            }
        )

        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(response_post.data['rating'], 4)

        self.login_user(self.user_verif)
        response_get= self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_get.data[0]['ido'], response_get.data[0]['ido'])

    def test_djiler_car_ratings(self):
        self.login_user(self.user_verif)
        car = Car.objects.create(user=self.user)
        url = reverse('reservations-driver', args=[self.user_verif.id])
        response_post = self.client.post(url, 
            {
                "date_from": "2022-05-30",
                "date_to": "2022-06-03",
                "status": "R",
                "driver": self.user_verif.id,
                "djiler": self.user.id,
                "car": car.idc
            }
        )

        self.login_user(self.user)
        url = reverse('ratings-car', args=[self.user.id])
        response_post = self.client.post(url,
            {
                "car_rating": 4,
                "djiler_rating": 4,
                "descr_djiler": "Dobar momak",
                "descr": "Kida!!!", 
                "idr": response_post.data['idr'],
                "idu": self.user_verif.id,
                "idd": self.user.id,
                "idc": car.idc
            }
        )        
        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(response_post.data['car_rating'], 4)
        self.assertEqual(response_post.data['djiler_rating'], 4)


        url = reverse('ratings-car', args=[car.idc])
        request = self.factory.get(url)
        response_get = CarRatingsView.as_view()(request, car.idc)
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_get.data[0]['idc'], car.idc)

        url = reverse('ratings-car', args=[self.user.id])
        request = self.factory.get(url)
        response_get = DjilerRatingsView.as_view()(request, self.user.id)
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_get.data[0]['idd'], self.user.id)

    
    def test_holdings(self):
        self.login_user(self.user_verif)
        car = Car.objects.create(user=self.user)
        reservation = Reservation.objects.create(
            date_from = datetime.datetime(2022,5,30),
            date_to = datetime.datetime(2022, 6, 3),
            status = 'R',
            idu=self.user_verif,
            idd=self.user,
            idc=car
        )
        holding = Holding.objects.create(
            idc = car,
            idr = reservation,
            price = 10,
            date_from = datetime.datetime(2022,5,30),
            date_to = datetime.datetime(2022, 6, 3)
        )

        url = reverse('reserved', args=[car.idc])
        request = self.factory.get(url)
        response = HoldingsView.as_view()(request, car.idc)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['date_from'], '2022-05-30')
        self.assertEqual(response.data[0]['date_to'], '2022-06-03')

    def test_ratings_get(self):
        self.login_user(self.user_verif)
        car = Car.objects.create(user=self.user)
        reservation = Reservation.objects.create(
            date_from = datetime.datetime(2022,5,30),
            date_to = datetime.datetime(2022,6,3),
            status = 'R',
            idu=self.user_verif,
            idd=self.user,
            idc=car
        )


        # Two grades for car and djiler
        self.login_user(self.user)
        for i in range(3):
            reservation = Reservation.objects.create(
                date_from = datetime.datetime(2022, 5+i, 30),
                date_to = datetime.datetime(2022, 6+i, 3),
                status = 'R',
                idu=self.user_verif,
                idd=self.user,
                idc=car
            )
            url = reverse('ratings-driver', args=[self.user_verif.id])
            response_post = self.client.post(url,
                {
                    "rating": 2+i,
                    "descr": "Kida!!!",
                    "idr": reservation.idr,
                    "idu": self.user_verif.id,
                    "idd": self.user.id
                }
            )
            url = reverse('ratings-car', args=[self.user.id])
            response_post = self.client.post(url,
                {
                    "car_rating": 2+i,
                    "djiler_rating": 2+i,
                    "descr_djiler": "Dobar momak",
                    "descr": "Kida!!!", 
                    "idr": reservation.idr,
                    "idu": self.user_verif.id,
                    "idd": self.user.id,
                    "idc": car.idc
                }
            )
        url = reverse('rating-car', args = [car.idc])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['rating'], 3.0)

        url = reverse('rating-driver', args = [self.user_verif.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['rating'], 3.0)

        url = reverse('rating-djiler', args = [self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['rating'], 3.0)



    
        





        
    
