from django.urls import path
from . import views

urlpatterns = [
    path(r'receta/',views.newReceta, name= 'newReceta'),
    path(r'doctor/',views.newDoctor, name= 'newDoctor'),
    path(r'healthform/', views.healthForm, name="healthForm"),
    path(r'fichamedica/', views.fichaMedica, name='fichaMedica'),
    path(r'turno/',views.newTurno, name='newTurno')
]



