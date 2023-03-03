from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    GENRE = (('M' ,'M'), ('F','F'))
    email = models.EmailField(_('email address'), unique=True)
    dob = models.DateField(blank= True, null = True)
    genre = models.CharField(null = False, blank= False ,max_length=10, choices=GENRE)

    username = None
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name','last_name')

    objects = CustomUserManager()

    def __str__(self):
        return self.email
