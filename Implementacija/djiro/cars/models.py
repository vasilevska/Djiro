from io import BytesIO
from tkinter import Image
from django.db import models
from django.core.files import File
from io import BytesIO
from PIL import Image

from users.models import User

class Manufacturer(models.Model):
    idman = models.AutoField(db_column='IdMan', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=20, blank=True, null=True)
    slug = models.SlugField()

    class Meta:
        managed = True
        db_table = 'manufacturer'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'


class Model(models.Model):
    idModel = models.AutoField(db_column = "IdModel", primary_key = True)
    manufacturer = models.ForeignKey(Manufacturer, models.DO_NOTHING, db_column='IdMan', blank = True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=20)
    slug = models.SlugField()

    class Meta:
        managed = True
        db_table = 'model'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'

class Car(models.Model):
    idc = models.AutoField(db_column='IdC', primary_key=True)  # Field name made lowercase.
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    km = models.IntegerField(blank=True, null=True)
    transmision = models.CharField(max_length=20, blank=True, null=True)
    fuel = models.CharField(max_length=20, blank=True, null=True)
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    images = models.ImageField(upload_to='uploads/', blank=True, null=True)
    descr = models.CharField(max_length=500, blank=True, null=True)
    model = models.ForeignKey(Model, models.DO_NOTHING, related_name='IdMan', db_column='IdMan', blank=True, null=True)  # Field name made lowercase.
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='id', blank=True, null=True)  # Field name made lowercase. # TODO: Changed db_column form IdU
    type = models.CharField(max_length=20, blank=True, null=True)
    slug = models.SlugField()
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'car'

    def __str__(self):
        return str(self.idc)

    def get_absolute_url(self):
        return f'/{self.slug}/'
    
    def get_image(self):
        if self.images:
            return 'http://127.0.0.1:8000' + self.images.url
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.images:
                self.thumbnail = self.make_thumbnail(self.images)
                self.save()
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''
    
    def make_thumbnail(self, images, size=(300,200)):
        img = Image.open(images)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=images.name)

        return thumbnail

        db_table = 'car'
