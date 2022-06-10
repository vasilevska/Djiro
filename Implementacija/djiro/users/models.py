"""
Autor/i: Stefan Branković 2019/0253, Aleksa Račić 2019/0728
"""
from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.files import File
from PIL import Image
from io import BytesIO
# Create your models here.

class Document(models.Model):
    """
    Models describings user's driving license
    """
    idd = models.AutoField(db_column='IdD', primary_key=True)  # Field name made lowercase.
    issuing_date = models.DateField(blank=True, null=True)
    valid_date = models.DateField(blank=True, null=True)
    issuing_place = models.CharField(max_length=50, blank=True, null=True)
    reg_number = models.CharField(max_length=20, blank=True, null=True)
    image1 = models.ImageField(upload_to="documents/", blank=True, null=True)
    image2 = models.ImageField(upload_to="documents/", blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'document'

    def get_image1(self):
        """
        Getter for the first side of the document
        Returns: image's url on the server
        """
        if self.image1:
            return "http://127.0.0.1:8000" + self.image1.url
        return ""

    def get_image2(self):
        """
        Getter for the second side of the document
        Returns: image's url on the server
        """
        if self.image2:
            return "http://127.0.0.1:8000" + self.image2.url
        return ""

class UserManager(BaseUserManager):
    """
    Model defining class to act as Manager class for creating User model objects
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Helper function for creating normal or superusers
        """
        if not email:
            raise ValueError(('The given email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """
        Function creating users with standard privileges
        """
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password,
                                 **extra_fields)

    def create_superuser(self,email, password, **extra_fields):
        """
        Function creating users with admin privileges
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self._create_user(email, password,
                                 **extra_fields)
        
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=False)
    last_name = models.CharField(max_length=30, blank=True, null=False)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, default="default.jpg")
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    email_verified = models.IntegerField(blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=False)
    bio = models.CharField(max_length=256, blank=True, null=True)
    doc_verified = models.BooleanField(default=False)
    is_djiler = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    idd = models.ForeignKey(Document, models.CASCADE, db_column='IdD', blank=True, null=True)  # Field name made lowercase.
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        managed = True
        db_table = 'user'

    def get_avatar(self):
        """
        Getter for user's avatar image
        """
        if self.avatar:
            return "http://127.0.0.1:8000" + self.avatar.url
        return ""

    def get_thumbnail(self):
        """
        Getter for user's thumbnail image (smaller size), made from of user's avatar image
        """
        if self.thumbnail:
            return "http://127.0.0.1:8000" + self.thumbnail.url
        else:
            if self.avatar:
                self.thumbnail = self.make_thumbnail(self.avatar)
                self.save()

                return "http://127.0.0.1:8000" + self.thumbnail.url
            else:
                return ""

    def make_thumbnail(self, image, size=(150,150)):
        """
        Helper function for creating copy of an image with modified size
        Returns: thumbnail - PIL image of wanted size
        """
        img = Image.open(image)
        img.convert("RGB")
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, "JPEG", quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


"""
class Passwordreset(models.Model):
    idpr = models.AutoField(db_column='IdPR', primary_key=True)  # Field name made lowercase.
    idu = models.ForeignKey('User', models.DO_NOTHING, db_column='IdU', blank=True, null=True)  # Field name made lowercase.
    token = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passwordreset'
"""

class Validacija(models.Model):
    """
    Model defining table that is used for validating user's submitted document by the admin
    """
    user = models.ForeignKey(User, models.CASCADE)
    document = models.ForeignKey(Document, models.CASCADE)
    verifikovan = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'validation'
    
    def getImage1(self):
        """
        Getter for the first side of the document
        """
        return self.document.get_image1()

    def getImage2(self):
        """
        Getter for the second size of the document
        """
        return self.document.get_image2()