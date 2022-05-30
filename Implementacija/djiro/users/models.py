from django.db import models

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

class User(models.Model):
    idu = models.AutoField(db_column='IdU', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.CharField(max_length=50, blank=True, null=True)
    email_verified = models.IntegerField(blank=True, null=True)
    token = models.CharField(max_length=50, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    bio = models.CharField(max_length=256, blank=True, null=True)
    username = models.CharField(max_length=20)
    doc_verified = models.IntegerField(blank=True, null=True)
    idd = models.ForeignKey(Document, models.DO_NOTHING, db_column='IdD', blank=True, null=True)  # Field name made lowercase.

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
