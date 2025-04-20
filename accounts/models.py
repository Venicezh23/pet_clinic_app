#Pet Owner account model
from django.contrib.auth.models import User
from django.db import models

class PetOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="Unnamed Owner")

    def __str__(self):
        return self.name
