from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

# Create your models here.

class Document(models.Model):
    idd = models.AutoField(db_column='IdD', primary_key=True)  # Field name made lowercase.
    issuing_date = models.DateField(blank=True, null=True)
    valid_date = models.DateField(blank=True, null=True)
    issuing_place = models.CharField(max_length=50, blank=True, null=True)
    reg_number = models.CharField(max_length=20, blank=True, null=True)
    image1 = models.CharField(max_length=50, blank=True, null=True)
    image2 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'document'


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(('The given email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password,
                                 **extra_fields)

    def create_superuser(self,email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self._create_user(email, password,
                                 **extra_fields)
        
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.CharField(max_length=50, blank=True, null=True)
    email_verified = models.IntegerField(blank=True, null=True)
    token = models.CharField(max_length=50, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    bio = models.CharField(max_length=256, blank=True, null=True)
    doc_verified = models.IntegerField(blank=True, null=True)
    is_djiler = models.BooleanField(default=False)
    idd = models.ForeignKey(Document, models.DO_NOTHING, db_column='IdD', blank=True, null=True)  # Field name made lowercase.

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        managed = True
        db_table = 'user'


"""
class Passwordreset(models.Model):
    idpr = models.AutoField(db_column='IdPR', primary_key=True)  # Field name made lowercase.
    idu = models.ForeignKey('User', models.DO_NOTHING, db_column='IdU', blank=True, null=True)  # Field name made lowercase.
    token = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passwordreset'
"""
