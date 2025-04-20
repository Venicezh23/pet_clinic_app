from django import forms
from .models import Appointment, Veterinarian

class AppointmentForm(forms.ModelForm):
    appt_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True
    )

    class Meta:
        model = Appointment
        fields = ["vet", "appt_datetime", "description", "status"]
