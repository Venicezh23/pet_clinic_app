from django.shortcuts import render, redirect
from pets.models import PetProfile
from pets.forms import PetProfileForm
from accounts.models import PetOwner
from django.contrib.auth.decorators import login_required

from google.cloud import storage
from google.oauth2 import service_account
from datetime import timedelta
from django.conf import settings

def generate_signed_url(blob_name):
    credentials = service_account.Credentials.from_service_account_file(
        settings.GS_CREDENTIALS
    )
    client = storage.Client(credentials=credentials, project=settings.GS_PROJECT_ID)
    bucket = client.bucket(settings.GS_BUCKET_NAME)
    blob = bucket.blob(blob_name)
    url = blob.generate_signed_url(
        expiration=timedelta(minutes=10),  # expires in 10 minutes
        method='GET'
    )
    return url

@login_required
def home(request):
    pets = []
    if request.user.is_authenticated:
        try:
            pet_owner = PetOwner.objects.get(user=request.user)  # Get PetOwner
            pets = PetProfile.objects.filter(owner=pet_owner)  # Get pets

            for pet in pets:
                if pet.photo and pet.photo.name:
                    pet.signed_url = generate_signed_url(pet.photo.name)
                else:
                    pet.signed_url = None
        except PetOwner.DoesNotExist:
            pets = []  # No PetOwner, return empty list

    return render(request, "home.html", {"pets": pets})

@login_required
def pet_list(request):
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


def add_pet(request):
    if request.method == "POST":
        form = PetProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the PetOwner associated with the logged-in user
            pet_owner = PetOwner.objects.get(user=request.user)

            # Set the owner of the pet profile as the PetOwner instance
            pet_profile = form.save(commit=False)
            pet_profile.owner = pet_owner  # Assign the PetOwner instance as the owner

            pet_profile.save()
            return redirect('home')
    else:
        form = PetProfileForm()
    return render(request, "pets/add_pet.html", {"form": form})