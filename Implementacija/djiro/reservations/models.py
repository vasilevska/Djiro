from django.db import models
from cars.models import Car

from users.models import User

# Create your models here.

class Reservation(models.Model):
    idr = models.AutoField(db_column='IdR', primary_key=True)  # Field name made lowercase.
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    idu = models.ForeignKey(User, models.DO_NOTHING, db_column='IdU', blank=True, null=True)  # Field name made lowercase.
    idc = models.ForeignKey(Car, models.DO_NOTHING, db_column='IdC', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'reservation'

class Ratingdriver(models.Model):
    ido = models.AutoField(db_column='IdO', primary_key=True)  # Field name made lowercase.
    rating = models.IntegerField(blank=True, null=True)
    idr = models.ForeignKey(Reservation, models.DO_NOTHING, db_column='IdR', blank=True, null=True)  # Field name made lowercase.
    idu = models.ForeignKey(User, models.DO_NOTHING, related_name='IdU', db_column='IdU', blank=True, null=True)  # Field name made lowercase.
    idd = models.ForeignKey(User, models.DO_NOTHING, related_name='IdD', db_column='IdD', blank=True, null=True)  # Field name made lowercase.
    descr = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ratingdriver'

class Ratingcar(models.Model):
    ido = models.AutoField(db_column='IdO', primary_key=True)  # Field name made lowercase.
    car_rating = models.IntegerField(blank=True, null=True)
    descr = models.CharField(max_length=500, blank=True, null=True)
    djiler_rating = models.IntegerField(blank=True, null=True)
    idr = models.ForeignKey(Reservation, models.DO_NOTHING, db_column='IdR', blank=True, null=True)  # Field name made lowercase.
    idc = models.ForeignKey(Car, models.DO_NOTHING, db_column='IdC', blank=True, null=True)  # Field name made lowercase.
    idd = models.ForeignKey(User, models.DO_NOTHING, db_column='IdD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ratingcar'

class Holding(models.Model):
    idc = models.ForeignKey(Car, models.DO_NOTHING, db_column='IdC')  # Field name made lowercase.
    idr = models.OneToOneField(Reservation, models.DO_NOTHING, db_column='IdR', primary_key=True)  # Field name made lowercase.
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'holding'