"""core URL Configuration
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from login.views import profile
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',include('login.urls')),
    path('home/',login_required(TemplateView.as_view(template_name = 'home/home.html')),name = 'home'),
    path('historia/',TemplateView.as_view(template_name = 'historia-clinica/historia.html'),name = 'historia'),
    path('novedades/',TemplateView.as_view(template_name = 'novedades/novedades.html'), name = 'novedades'),
    path('perfil/',profile, name = 'perfil'),
    path('notificaciones/',TemplateView.as_view(template_name = 'notificaciones/notificaciones.html'),name = 'notificaciones'),
    path('health/',include('health.urls')),
    path('',TemplateView.as_view(template_name = 'landing/landing.html'),name = 'landing'),
    path('dashboard/',include('dashboard.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
