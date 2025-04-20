from django.contrib import admin
from .models import Veterinarian, Appointment

#can add Veterinarian manually from here
admin.site.register(Veterinarian)
admin.site.register(Appointment)
