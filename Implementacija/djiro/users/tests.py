from django.contrib.auth.models import AnonymousUser
from django.utils.http import urlencode
from django.urls import reverse
from django.test import RequestFactory, TestCase
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from PIL import Image
from io import BytesIO
import datetime

from .models import User
from .views import RetrieveIdView, RetrieveUser, UserRegistration

class UsersTest(TestCase):
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

    def logout_user(self):
        # Delete the saved access token for logout
        self.client.credentials(HTTP_AUTHORIZATION='')

    def retrieve_id_view(self):
        # Create an instance of a GET request.
        url = reverse('get-id')
        response = self.client.get(url)

        return response

    def get_mock_img(self, name='test.jpeg', ext='jpeg', size=(50, 50)):
        byte_obj = BytesIO()
        image = Image.new(mode="RGB", size=size)
        image.save(byte_obj, ext)
        byte_obj.seek(0)
        return byte_obj.read()

    def test_retrieve_id_view_not_login(self):
        response = self.retrieve_id_view()
        self.assertEqual(response.status_code, 401)

    def test_retrieve_id_view_login(self):
        self.login_user()
        response = self.retrieve_id_view()
        self.assertEqual(response.status_code, 200)

    def test_retrieve_user(self):
        url = reverse('get-user')        
        request = self.factory.get(url, {"id": self.user.id})

        response = RetrieveUser.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
    
    def test_retrieve_user_empty(self):
        url = reverse('get-user')        
        request = self.factory.get(url, {"id": -1})

        response = RetrieveUser.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 0)

    def test_update_user_info_tel(self):
        self.login_user()
        url = reverse('update-user', args=[self.user.id])
        response = self.client.post(url, 
        {"first_name": "jacob", "last_name": "jacobs", "tel": "000"})
        self.assertEqual(response.status_code, 400)

    def test_update_user_info(self):
        self.login_user()
        url = reverse('update-user', args=[self.user.id])
        response = self.client.post(url, 
        {"first_name": "jacob", "last_name": "jacobs", "tel": "0645779704"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['first_name'], "jacob")
        self.assertEqual(response.data['last_name'], "jacobs")
        self.assertEqual(response.data['tel'], "0645779704")

    def test_update_avatar_fail(self):
        self.login_user()
        url = reverse('update-avatar', args=[self.user.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)

    def test_update_avatar(self):
        self.login_user()
        url = reverse('update-avatar', args=[self.user.id])

        photo = SimpleUploadedFile("photo.jpeg", self.get_mock_img(), content_type="image/jpeg")

        response = self.client.post(url, data={'avatar': photo}
        ,headers={ "Content-Type": "multipart/form-data" })
        self.assertEqual(response.status_code, 201)

    def test_registration_success(self):
        url = reverse('registration')

        request = self.factory.post(url, {"email": "janko@gmail.com","first_name": "janko", "last_name": "jankovic",
         "password1" :"jankulajankula", "password2" :"jankulajankula", "tel": "0645553333"})
        
        response = UserRegistration.as_view()(request)
        
        self.assertEqual(response.status_code, 201)

    def test_registration_password_common(self):
        url = reverse('registration')
        request = self.factory.post(url, {"email": "janko@gmail.com","first_name": "janko", "last_name": "jankovic",
         "password1" :"asdfasdf", "password2" :"asdfasdf", "tel": "0645553333"})
        
        response = UserRegistration.as_view()(request)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password1'][0].title(), 'This Password Is Too Common.')

    def test_registration_blank(self):
        url = reverse('registration')
        request = self.factory.post(url, {"first_name": "", "last_name": "",
         "password1" :"", "password2" :"", "tel": "0645553333"})
        
        response = UserRegistration.as_view()(request)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['email'][0].title(), 'This Field Is Required.')
        self.assertEqual(response.data['first_name'][0].title(), 'This Field May Not Be Blank.')
        self.assertEqual(response.data['last_name'][0].title(), 'This Field May Not Be Blank.')
        self.assertEqual(response.data['password1'][0].title(), 'This Field May Not Be Blank.')
        self.assertEqual(response.data['password2'][0].title(), 'This Field May Not Be Blank.')

    def test_registration_pass_match(self):
        url = reverse('registration')
        request = self.factory.post(url, {"email": "janko@gmail.com","first_name": "janko", "last_name": "jankovic",
         "password1" :"jankulajankula", "password2" :"jankula", "tel": "0645553333"})
        
        response = UserRegistration.as_view()(request)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0].title(), "The Two Password Fields Didn'T Match.")

    def test_registration_success(self):
        url = reverse('registration')
        request = self.factory.post(url, {"email": "janko@gmail.com","first_name": "janko", "last_name": "jankovic",
         "password1" :"jankulajankula", "password2" :"jankulajankula", "tel": "064"})
        
        response = UserRegistration.as_view()(request)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0].title().lower(), 
        "please insert telephone in the correct 10-digit format")

    def test_vozacka_validation_success(self):
        self.login_user()

        url = reverse('verify-vozacka')
        issuing_date = datetime.date(2010,1,1)
        valid_date= datetime.date(2014,1,1)
        image1 = SimpleUploadedFile("photo.jpeg", self.get_mock_img(), content_type="image/jpeg")
        image2 = SimpleUploadedFile("photo.jpeg", self.get_mock_img(), content_type="image/jpeg")

        response = self.client.post(url, {"issuing_date": issuing_date,
        "valid_date": valid_date,"issuing_place": "Beograd","reg_number" :"000111222",
        "image1": image1, "image2": image2},headers={ "Content-Type": "multipart/form-data" })

        self.assertEqual(response.status_code, 201)
    
    def test_vozacka_validation_fail_img1(self):
        self.login_user()

        url = reverse('verify-vozacka')
        issuing_date = datetime.date(2010,1,1)
        valid_date= datetime.date(2014,1,1)
        
        image2 = SimpleUploadedFile("photo.jpeg", self.get_mock_img(), content_type="image/jpeg")

        response = self.client.post(url, {"issuing_date": issuing_date,
        "valid_date": valid_date,"issuing_place": "Beograd","reg_number" :"000111222",
        "image2": image2},headers={ "Content-Type": "multipart/form-data" })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0].title().lower(), 
        "nema slike 1")

    def test_vozacka_validation_fail_img2(self):
        self.login_user()

        url = reverse('verify-vozacka')
        issuing_date = datetime.date(2010,1,1)
        valid_date= datetime.date(2014,1,1)
        image1 = SimpleUploadedFile("photo.jpeg", self.get_mock_img(), content_type="image/jpeg")
    

        response = self.client.post(url, {"issuing_date": issuing_date,
        "valid_date": valid_date,"issuing_place": "Beograd","reg_number" :"000111222",
        "image1": image1},headers={ "Content-Type": "multipart/form-data" })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0].title().lower(), 
        "nema slike 2")
        