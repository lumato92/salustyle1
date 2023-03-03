from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django import forms
from .models import CustomUser

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Password Confirmation'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'

        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email','dob','genre', 'password1', 'password2' )
        help_texts = {
            'username': None,
        }

class PerfilForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'dob','genre')
        help_texts = {
            'username': None,
        }

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class ChangePasswordForm(PasswordChangeForm):

    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']

class ResetPasswordForm(SetPasswordForm):
    
    class Meta:
        model = CustomUser
        fields = ['new_password1', 'new_password2']
        







