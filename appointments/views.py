from django.shortcuts import render, get_object_or_404, redirect
from .models import Appointment, Veterinarian
from pets.models import PetProfile
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from accounts.models import PetOwner

from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import timedelta
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
        pet_owner = PetOwner.objects.get(user=request.user)  # Get the PetOwner instance
        owner_pets = PetProfile.objects.filter(owner=pet_owner)  # Get all pets belonging to the owner
        
        selected_pet_id = request.GET.get('pet_id')  # Get pet_id from the dropdown

        if selected_pet_id:  # If a pet is selected, filter appointments by that pet
            appointments = Appointment.objects.filter(pet__id=selected_pet_id, pet__owner=pet_owner)
        else:  # Otherwise, show all appointments for the pet owner
            appointments = Appointment.objects.filter(pet__owner=pet_owner)

        #check for appointments one day away from the current date
        one_day_away = timezone.now().date() + timedelta(days=1)
        upcoming_appointments = appointments.filter(appt_datetime__date=one_day_away)

    except PetOwner.DoesNotExist:
        appointments = Appointment.objects.none()  # If the user has no pet, return empty
        owner_pets = []  # No pets available
        upcoming_appointments = []

    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments,
        'owner_pets': owner_pets,
        'selected_pet_id': selected_pet_id,
        'upcoming_appointments':upcoming_appointments,
    })

