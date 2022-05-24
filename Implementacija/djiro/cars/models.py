from django.db import models

# Create your models here.

from users.models import User

class Manufacturer(models.Model):
    idman = models.AutoField(db_column='IdMan', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'manufacturer'


class Model(models.Model):
    idman = models.OneToOneField(Manufacturer, models.DO_NOTHING, db_column='IdMan', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'model'
        unique_together = (('idman', 'name'),)

class Car(models.Model):
    idc = models.AutoField(db_column='IdC', primary_key=True)  # Field name made lowercase.
    coordinates = models.CharField(max_length=20, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    km = models.IntegerField(blank=True, null=True)
    transmision = models.CharField(max_length=20, blank=True, null=True)
    fuel = models.CharField(max_length=20, blank=True, null=True)
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    images = models.CharField(max_length=100, blank=True, null=True)
    descr = models.CharField(max_length=500, blank=True, null=True)
    idman = models.ForeignKey(Model, models.DO_NOTHING, related_name='IdMan', db_column='IdMan', blank=True, null=True)  # Field name made lowercase.
    idu = models.ForeignKey(User, models.DO_NOTHING, db_column='IdU', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(max_length=20, blank=True, null=True)
    model = models.ForeignKey(Model, models.DO_NOTHING, related_name='Model', db_column='name', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'car'