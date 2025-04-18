from django.contrib import admin
from pets.models import PetProfile, MedicalRecord, Vaccination, Vaccine  # Ensure this is correct

admin.site.register(PetProfile)  # Ensure this is the correct model
admin.site.register(MedicalRecord)
admin.site.register(Vaccination)
admin.site.register(Vaccine)
