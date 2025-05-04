from django.shortcuts import render, redirect
from pets.models import PetProfile
from pets.forms import PetProfileForm
from accounts.models import PetOwner
from django.contrib.auth.decorators import login_required

from google.cloud import storage
from google.oauth2 import service_account
from datetime import timedelta
from django.conf import settings

#generate urls for photos using GS credentials - link to cloud storage
def generate_signed_url(blob_name):
    credentials = settings.GS_CREDENTIALS
    client = storage.Client(credentials=credentials, project=settings.GS_PROJECT_ID)
    bucket = client.bucket(settings.GS_BUCKET_NAME)
    blob = bucket.blob(blob_name)
    url = blob.generate_signed_url(
        expiration=timedelta(minutes=10),  #expires in 10 minutes
        method='GET'
    )
    return url

@login_required
def home(request):
    pets = []
    if request.user.is_authenticated:
        try: #if pet owner exists, get any pets they have
            pet_owner = PetOwner.objects.get(user=request.user)
            pets = PetProfile.objects.filter(owner=pet_owner)

            for pet in pets:
                if pet.photo and pet.photo.name:
                    pet.signed_url = generate_signed_url(pet.photo.name)
                else:
                    pet.signed_url = None
        except PetOwner.DoesNotExist:
            pets = []

    return render(request, "home.html", {"pets": pets})

@login_required
def pet_list(request): #display all pets an owner has
    try:
        pet_owner = PetOwner.objects.get(user=request.user)
        pets = PetProfile.objects.filter(owner=pet_owner)

        for pet in pets:
            if pet.photo and pet.photo.name:
                pet.signed_url = generate_signed_url(pet.photo.name)
            else:
                pet.signed_url = None

    except PetOwner.DoesNotExist:
        pets = []

    return render(request, "pets/pet_list.html", {"pets": pets})

def add_pet(request): #add pet and assign to current user
    if request.method == "POST":
        form = PetProfileForm(request.POST, request.FILES)
        if form.is_valid():
            pet_owner = PetOwner.objects.get(user=request.user)
            pet_profile = form.save(commit=False)
            pet_profile.owner = pet_owner
            pet_profile.save()
            return redirect('home')
    else:
        form = PetProfileForm()
    return render(request, "pets/add_pet.html", {"form": form})

