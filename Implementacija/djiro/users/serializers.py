from rest_framework import serializers
from allauth.account.adapter import get_adapter
from djiro import settings
from .models import User
from allauth.account.utils import setup_user_email
import re
from .models import *


class DocumentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            "idd",
            "issuing_date",
            "valid_date",
            "issuing_place",
            "reg_number",
            "image1",
            "image2"
        )

    def validate(self, data):
        print(data)
        if not data['image1']:
            raise serializers.ValidationError(
                ("Nema slike 1"))

        if not data['image2']:
            raise serializers.ValidationError(
                ("Nema slike 2"))

        return data
    
    def get_cleaned_data(self):
        return {
            'issuing_date': self.validated_data.get('issuing_date', ''),
            'valid_date': self.validated_data.get('valid_date', ''),
            'issuing_place': self.validated_data.get('issuing_place', ''),
            'reg_number': self.validated_data.get('reg_number', ''),
            'image1': self.validated_data.get('image1', ''),
            'image2': self.validated_data.get('image2', ''),
        }

    def save(self, request):
        doc = Document()
        self.cleaned_data = self.get_cleaned_data()
        doc.issuing_date = self.cleaned_data['issuing_date']
        doc.valid_date = self.cleaned_data['valid_date']
        doc.issuing_place = self.cleaned_data['issuing_place']
        doc.reg_number = self.cleaned_data['reg_number']
        
        doc.image1 = request.FILES['image1']
        doc.image2 = request.FILES['image2']

        doc.save()

        user = User.objects.get(email=request.user)

        Validacija(user = user, document = doc).save()
        
        return doc
    

class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'email',
                  'email_verified', 'tel', 'doc_verified', 'is_djiler',
                 'bio', 'get_avatar', 'get_thumbnail', 'idd')
        read_only_fields = ('email', )


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Author: Stefan Brankovic 2019/0253
    """
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)

    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    

    class Meta:
        model = User
        fields = ('pk', 'email', 'first_name', 'last_name', 'password1', 'password2', 'tel', 'bio',
        'avatar')

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        prog = re.compile(r"^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$")
        if 'password1' in data and data['password1'] != data['password2']:
            raise serializers.ValidationError(
                ("The two password fields didn't match."))
        elif data['tel'] != "" and prog.match(data['tel']) is None:
            raise serializers.ValidationError(
                ("Please insert telephone in the correct 10-digit format"))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'avatar': self.validated_data.get('avatar', ''),
            'tel': self.validated_data.get('tel', ''),
            'bio': self.validated_data.get('bio', ''),
        }


    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        
        user.is_djiler = False
        user.email_verified = True
        user.doc_verified= True

        if 'avatar' in request.FILES and request.FILES['avatar'] != '':
            user.avatar = request.FILES['avatar']
        user.tel = self.cleaned_data['tel']
        user.bio = self.cleaned_data['bio']

        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'tel', 'bio',
        'avatar')

    def validate(self, data):
        prog = re.compile(r"^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$")
        if data['tel'] != "" and prog.match(data['tel']) is None:
            raise serializers.ValidationError(
                ("Please insert telephone in the correct 10-digit format"))
        return data

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.tel = validated_data.get('tel', instance.tel)
        instance.bio = validated_data.get('bio', instance.bio)