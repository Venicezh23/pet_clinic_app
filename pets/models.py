from django.db import models
#from .models import Vaccine
from accounts.models import PetOwner
from appointments.models import Appointment, Veterinarian

def pet_photo_upload_path(instance, filename):
    return f'pet_photos/{instance.owner.id}_{instance.name}_{filename}'

class PetProfile(models.Model):
    owner = models.ForeignKey(PetOwner, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='pet_photos/', blank=True, null=True)
    medical_record = models.OneToOneField('MedicalRecord', on_delete=models.CASCADE, null=True, blank=True)
    appointment = models.ForeignKey("appointments.Appointment", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class MedicalRecord(models.Model):
    medical_record_ID = models.AutoField(primary_key=True)
    pet = models.ForeignKey('pets.PetProfile', on_delete=models.CASCADE, related_name='medical_records', null=True, blank=True)
    vaccines = models.ManyToManyField("Vaccine", through="Vaccination")
    clinic_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Medical Record {self.medical_record_ID} - {self.pet.name}"

#Note: Vaccines are added manually via /admin for simplicity of app
class Vaccination(models.Model):
    vaccination_ID = models.AutoField(primary_key=True)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name="vaccinations")
    vaccine = models.ForeignKey("Vaccine", on_delete=models.CASCADE)
    date_administered = models.DateField()
    date_expiry = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.vaccine.name} - {self.date_administered.strftime('%b %Y')}"

class Vaccine(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name