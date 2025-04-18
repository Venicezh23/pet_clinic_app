from django.db import models
#from pets.models import PetProfile
from accounts.models import PetOwner

class Veterinarian(models.Model):
    name = models.CharField(max_length=255)
    expertise = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ]

    vet = models.ForeignKey("appointments.Veterinarian", on_delete=models.CASCADE, related_name='appointments')
    pet = models.ForeignKey("pets.PetProfile", on_delete=models.CASCADE, related_name='appointments')
    appt_datetime = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='booked')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Appointment with {self.vet.name} for {self.pet.name} on {self.appt_datetime}"
