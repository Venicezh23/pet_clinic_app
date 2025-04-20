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
    veterinarians = Veterinarian.objects.all()  #get all veterinarians available

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.pet = pet
            appointment.save()
            return redirect("home")  #go back to home page
    else:
        form = AppointmentForm()

    return render(request, "appointments/book_appointment.html", {"form": form, "pet": pet, "veterinarians": veterinarians})

@login_required
def edit_appointment(request, appointment_id):
    pet_owner = get_object_or_404(PetOwner, user=request.user)
    appointment = get_object_or_404(Appointment, id=appointment_id, pet__owner=pet_owner)

    class EditAppointmentForm(AppointmentForm):
        class Meta(AppointmentForm.Meta):
            fields = AppointmentForm.Meta.fields + ['status']

    if request.method == "POST":
        form = EditAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect("appointments:appointment_list")
        
    else:
        form = EditAppointmentForm(instance=appointment)
    return render(request, "appointments/edit_appointment.html", {"form": form, "appointment": appointment})

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

        #get appointments within 24 hours
        now = timezone.now()
        next_24_hours = now + timedelta(hours=24)
        upcoming_appointments = appointments.filter(
            appt_datetime__gte=now, appt_datetime__lte=next_24_hours
            ).exclude(status__in=['Done', 'Cancelled'])
        
        upcoming_appointment_ids = list(upcoming_appointments.values_list('id', flat=True))

    except PetOwner.DoesNotExist:
        appointments = Appointment.objects.none()
        owner_pets = []
        upcoming_appointments = []

    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments,
        'owner_pets': owner_pets,
        'selected_pet_id': selected_pet_id,
        'upcoming_appointments': upcoming_appointments,
        'upcoming_appointments_ids': upcoming_appointment_ids
    })