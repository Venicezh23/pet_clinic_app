from django.db import models
#from .models import Vaccine
from accounts.models import PetOwner
from appointments.models import Appointment, Veterinarian

def pet_photo_upload_path(instance, filename):
    return f'pet_photos/{instance.owner.id}_{instance.name}_{filename}'

class PetProfile(models.Model):
    #pet_ID = models.AutoField(primary_key=True)
    #owner = models.ForeignKey(PetOwner, on_delete=models.CASCADE, related_name="pets")
    owner = models.ForeignKey(PetOwner, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    #age = models.IntegerField()
    dob = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='pet_photos/', blank=True, null=True)
    medical_record = models.OneToOneField('MedicalRecord', on_delete=models.CASCADE, null=True, blank=True)
    appointment = models.ForeignKey("appointments.Appointment", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

####NOTE: need to check if can reference pet as PET_ID?
class MedicalRecord(models.Model):
    medical_record_ID = models.AutoField(primary_key=True)
    #note: to remove null-True and blank=True
    pet = models.ForeignKey('pets.PetProfile', on_delete=models.CASCADE, related_name='medical_records', null=True, blank=True)
    #appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    #vet = models.ForeignKey(Veterinarian, on_delete=models.SET_NULL, null=True, blank=True)
    vaccines = models.ManyToManyField("Vaccine", through="Vaccination")
    clinic_name = models.CharField(max_length=255, null=True, blank=True)
    #vet_name = models.CharField(max_length=255, null=True, blank=True)  # Allow manual vet input

    def __str__(self):
        return f"Medical Record {self.medical_record_ID} - {self.pet.name}"

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