from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('userlogin/',views.loginUser, name= 'loginUser'),
    path('register/', views.newUser, name = 'newUser'),
    path('testing/', views.loginTestingPage, name= 'testing'),
    path('changepassword/',views.passwordChange, name= 'passwordChange'),
    
    path('activate/<uidb64>/<token>',views.activate, name='activate'),

    path('recoveruser/', views.recoverPass, name = 'recoverPass'),
    path('resetpassword/<uidb64>/<token>',views.resetPassword, name ='resetearPassword'),
    
     path('logout/',LogoutView.as_view(template_name='login/logout.html'),name='logout'),
]
