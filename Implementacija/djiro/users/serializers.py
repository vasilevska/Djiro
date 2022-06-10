"""
Autor/i: Stefan Branković 2019/0253, Aleksa Račić 2019/0728
"""
from rest_framework import serializers
from allauth.account.adapter import get_adapter
from djiro import settings
from .models import User
from allauth.account.utils import setup_user_email
import re
from .models import *


class DocumentDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user's document details
    """
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
        """
        Args:
            data: dict = unvalidated input data
        Returns:
            data: dict 
        """
        if 'image1' not in data or not data['image1']:
            raise serializers.ValidationError(
                ("Nema slike 1"))

        if 'image2' not in data or not data['image2']:
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
        """
        Args:
            request: dict = HTTP request containing Document's fields info
        Returns:
            doc : Document = created Document object
        """
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
    Serializer for user registration
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
        """
        Args: 
            password: string
        Returns: validated password
        """
        return get_adapter().clean_password(password)

    def validate(self, data):
        """Passwords must match and phone number should be in one of the following formats (includes some more):
            18005551234
            1 800 555 1234
            +1 800 555-1234
            +86 800 555 1234
            1-800-555-1234
            1 (800) 555-1234
            (800)555-1234
            (800) 555-1234
            (800)5551234
            800-555-1234
        Args:
            data: dict
        Returns:
            data: dict
        """
        prog = re.compile(r"^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$")
        if 'password1' in data and data['password1'] != data['password2']:
            raise serializers.ValidationError(
                ("The two password fields didn't match."))
        elif data['tel'] != "" and prog.match(data['tel']) is None:
            raise serializers.ValidationError(
                ("Please insert telephone in the correct 10-digit format"))
        return data

    def get_cleaned_data(self):
        """
        Helper function that returns validated data field or an empty string
        """
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
        """
        Args:
            request: dict = HTTP request containing User's fields info
        """
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
    """
    Serializer used for updating user's info (password and email are excluded)
    """
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