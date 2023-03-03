from django.urls import path
from dashboard import views



urlpatterns = [
    path(r'mainpage/',views.mainPage, name= 'mainPage'),
    path(r'test/',views.test),
    path(r'turnomodal/',views.newTurno,name="turnoModal"),
    path('doctorTest', views.DoctorCreateView.as_view(),name='newDoctorTest')
]