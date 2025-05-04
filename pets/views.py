from django.shortcuts import render, redirect, get_object_or_404
from .models import PetProfile, MedicalRecord, Vaccination, Vaccine
from .forms import PetProfileForm, MedicalRecordForm, VaccinationForm
from accounts.models import PetOwner #reference to pet owner
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory

from google.cloud import storage
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import timedelta

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@login_required
def add_pet_profile(request):
    if not hasattr(request.user, 'petowner'): #check if petowner exists
        return redirect("register") #redirect to register pg

    if request.method == "POST":
        print("FILES:", request.FILES) #debug print
        form = PetProfileForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            pet = form.save(commit=False)
            pet.owner = request.user.petowner  #assign logged in user as pet owner
            pet.save()
            logger.info(f"User '{request.user.username}' added pet: ID={pet.id}, Name={pet.name}")
            print("Pet saved:", pet.id, pet.name, pet.photo)
            return redirect('home') #homepage
    else:
        form = PetProfileForm()

    return render(request, "pets/add_pet.html", {"form": form})

@login_required
def edit_pet_profile(request, pet_id):
    #pet owner that was logged in
    pet_owner = get_object_or_404(PetOwner, user=request.user)

    #filter pet profile
    pet = get_object_or_404(PetProfile, id=pet_id, owner=pet_owner)

    if request.method == "POST":
        form = PetProfileForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            logger.info(f"User '{request.user.username}' edited pet: ID={pet.id}, Name={pet.name}")
            return redirect('home')
    else:
        form = PetProfileForm(instance=pet)

    return render(request, 'pets/edit_pet_profile.html', {'form': form, 'pet': pet})

@login_required
def medical_record_list(request):
    selected_pet_id = request.GET.get('pet_id')

    try:
        pet_owner = PetOwner.objects.get(user=request.user)
    except PetOwner.DoesNotExist:
        pet_owner = None

    if pet_owner:
        owner_pets = PetProfile.objects.filter(owner=pet_owner)
        medical_records = MedicalRecord.objects.filter(pet__owner=pet_owner)

        if selected_pet_id:
            medical_records = medical_records.filter(pet__id=selected_pet_id)
    else:
        owner_pets = PetProfile.objects.none()
        medical_records = MedicalRecord.objects.none()

    return render(request, 'pets/medical_record_list.html', {
        'medical_records': medical_records,
        'owner_pets': owner_pets,
        'selected_pet_id': selected_pet_id,
    })



def add_medical_record(request, pet_id):
    pet = get_object_or_404(PetProfile, pk=pet_id)
    vaccines = Vaccine.objects.all()

    if request.method == 'POST':
        clinic_name = request.POST.get('clinic_name')
        vaccine_ids = request.POST.getlist('vaccines')
        date_administered = request.POST.get('date_administered')

        medical_record = MedicalRecord.objects.create(
            pet=pet,
            clinic_name=clinic_name,
        )

        for vaccine_id in vaccine_ids:
            vaccine = Vaccine.objects.get(pk=vaccine_id)
            Vaccination.objects.create(
                medical_record=medical_record,
                vaccine=vaccine,
                date_administered=f"{date_administered}-01"
            )

        return redirect('home')

    context = {
        'pet': pet,
        'vaccines': vaccines,
    }
    return render(request, 'pets/add_medical_record.html', context)

def add_vaccination(request):
    if request.method == 'POST':
        form = VaccinationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pets:medical_record_list') #go back to medical record table
    else:
        form = VaccinationForm()
    return render(request, 'pets/add_vaccination.html', {'form': form})


VaccinationFormSet = inlineformset_factory(
    MedicalRecord,
    Vaccination,
    form=VaccinationForm,
    extra=1,
    can_delete=True
)