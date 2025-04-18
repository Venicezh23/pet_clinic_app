from django.db import models
from appointments.models import Appointment

class Notification(models.Model):
    appt = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='notifications')
    notif_datetime = models.DateTimeField()

    def __str__(self):
        return f"Reminder for {self.appt.pet.name} on {self.notif_datetime}"

