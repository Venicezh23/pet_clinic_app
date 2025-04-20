from django.urls import path
from . import views
from .views import appointment_list, book_appointment

app_name = 'appointments'

urlpatterns = [
    path('book/<int:pet_id>/', book_appointment, name='book_appointment'),
    path('', appointment_list, name="appointment_list"),
    path('edit/<int:appointment_id>/', views.edit_appointment, name="edit_appointment"),
]
