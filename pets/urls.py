from django.urls import path
from .views import medical_record_list, add_medical_record, add_vaccination, edit_pet_profile

app_name = 'pets' #placeholder - need to add in for url referencing

urlpatterns = [
    path('medical-records/', medical_record_list, name='medical_record_list'),
    path('add-medical-record/', add_medical_record, name='add_medical_record'),
    path('add-vaccination/', add_vaccination, name='add_vaccination'),
    path('pets/<int:pet_id>/add-medical-record/', add_medical_record, name='add_medical_record'),
    path('pet/<int:pet_id>/edit/', edit_pet_profile, name='edit_pet_profile'),
    
]
