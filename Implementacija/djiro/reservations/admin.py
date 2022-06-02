from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Reservation)
admin.site.register(Ratingcar)
admin.site.register(Ratingdriver)
admin.site.register(Holding)