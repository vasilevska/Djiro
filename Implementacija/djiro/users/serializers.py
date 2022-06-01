from rest_framework import serializers
from allauth.account.adapter import get_adapter
from djiro import settings
from .models import User
from allauth.account.utils import setup_user_email

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
            "get_image1",
            "get_image2"
        )


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
    avatar = serializers.ImageField(required=True)

    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    

    class Meta:
        model = User
        fields = ('pk', 'email', 'first_name', 'last_name', 'password1', 'password2', 'tel', 'bio',
        'avatar')

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                ("The two password fields didn't match."))
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

        user.avatar = request.FILES['avatar']
        user.tel = self.cleaned_data['tel']
        user.bio = self.cleaned_data['bio']

        user.save()
        return user

