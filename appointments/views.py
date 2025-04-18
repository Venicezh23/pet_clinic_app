from django.shortcuts import render, get_object_or_404, redirect
from .models import Appointment, Veterinarian
from pets.models import PetProfile
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from accounts.models import PetOwner

from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import timedelta

from django.utils.timezone import make_aware, get_current_timezone

from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

@login_required
def book_appointment(request, pet_id):
    pet = get_object_or_404(PetProfile, id=pet_id, owner=request.user.petowner)
    veterinarians = Veterinarian.objects.all()  # Get all available veterinarians

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.pet = pet
            appointment.save()
            return redirect("home")  # Redirect to home page after booking
    else:
        form = AppointmentForm()

    return render(request, "appointments/book_appointment.html", {"form": form, "pet": pet, "veterinarians": veterinarians})

@login_required
def appointment_list(request):
    try:
        pet_owner = PetOwner.objects.get(user=request.user)
        owner_pets = PetProfile.objects.filter(owner=pet_owner)
        selected_pet_id = request.GET.get('pet_id')

        if selected_pet_id:
            appointments = Appointment.objects.filter(pet__id=selected_pet_id, pet__owner=pet_owner)
        else:
            appointments = Appointment.objects.filter(pet__owner=pet_owner)

        # Appointments due within the next 24 hours
        now = timezone.now()
        next_24_hours = now + timedelta(hours=24)
        upcoming_appointments = appointments.filter(appt_datetime__gte=now, appt_datetime__lte=next_24_hours)

    except PetOwner.DoesNotExist:
        appointments = Appointment.objects.none()
        owner_pets = []
        upcoming_appointments = []

    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments,
        'owner_pets': owner_pets,
        'selected_pet_id': selected_pet_id,
        'upcoming_appointments': upcoming_appointments,
    })