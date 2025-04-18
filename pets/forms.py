from django import forms
from .models import PetProfile, MedicalRecord, Vaccination, Vaccine

class PetProfileForm(forms.ModelForm):
    dob = forms.DateField (
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type':'date'}),
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
        required=False
    )

    class Meta:
        model = PetProfile
        fields = ["name", "breed", "dob", "photo"]

    def save(self, commit=True):
        # Automatically set the owner to the currently logged-in user
        pet_profile = super().save(commit=False)
        pet_profile.owner = self.instance.owner  # Set the owner from the instance (usually the logged-in user)
        
        if commit:
            pet_profile.save()
        return pet_profile

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['clinic_name', 'vaccines']  # Removed 'appointment', 'vet'

class VaccinationForm(forms.ModelForm):
    class Meta:
        model = Vaccination
        fields = ['vaccine', 'date_administered', 'date_expiry']

