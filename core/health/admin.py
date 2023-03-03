from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Turno)
admin.site.register(Receta)
admin.site.register(Health)
admin.site.register(Vacuna)
admin.site.register(Enf_Preexistentes)