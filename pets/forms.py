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
        #pet profile created linked to pet owner
        pet_profile = super().save(commit=False)
        pet_profile.owner = self.instance.owner  #set owner instance
        
        if commit:
            pet_profile.save()
        return pet_profile

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['clinic_name', 'vaccines']

class VaccinationForm(forms.ModelForm):
    class Meta:
        model = Vaccination
        fields = ['vaccine', 'date_administered', 'date_expiry']

