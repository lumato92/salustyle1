from django import forms 
from .models import Health, Receta, Doctor, Turno

from bootstrap_modal_forms.forms import BSModalModelForm


CHOICE = (('si' ,'Sí'), ('no','No'))

BLOOD_TYPE = (('O-','O-'),('O+', 'O+'),('A-','A-'),('A+','A+'),('B-','B-'),('B+','B+'),('AB-','AB-'),('AB+','AB+'))

class HealthForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HealthForm, self).__init__(*args, **kwargs)
        self.fields['height'].widget = forms.NumberInput(attrs={'class':'form-control common-input-bkg'})
        self.fields['weight'].widget = forms.NumberInput(attrs={'class':'form-control common-input-bkg'})
        self.fields['sedentary_work'].widget = forms.Select(attrs={'class':'form-control common-input-bkg'}, choices= CHOICE)
        self.fields['smoker'].widget = forms.Select(attrs={'class':'form-control common-input-bkg'}, choices= CHOICE)
        self.fields['blood_type'].widget = forms.Select(attrs={'class': 'form-control common-input-bkg'},choices= BLOOD_TYPE)
        self.fields['insurance'].widget = forms.TextInput(attrs={'class':'form-control common-input-bkg'})

    class Meta:
        model = Health
        fields = ('height','weight','sedentary_work','smoker','blood_type','insurance')



class RecetaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RecetaForm, self).__init__(*args, **kwargs)
        self.fields['prescription'].widget = forms.TextInput(attrs={'class' : 'form-control common-input-bkg'})
        self.fields['prescription_img'].widget = forms.FileInput(attrs={'class' : 'form-control '})
    class Meta:
        model = Receta
        fields = ("prescription", "prescription_img")


class DoctorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(DoctorForm,self).__init__(*args, **kwargs)
        self.fields['md_fullname'].widget = forms.TextInput(attrs={'class' : 'form-control common-input-bkg'})
        self.fields['md_specialize'].widget = forms.TextInput(attrs={'class' : 'form-control common-input-bkg'})
        self.fields['md_contactphone'].widget = forms.TextInput(attrs={'class' : 'form-control common-input-bkg'})
        self.fields['md_mail'].widget = forms.EmailInput(attrs={'class' : 'form-control common-input-bkg'})
        self.fields['md_address'].widget = forms.TextInput(attrs={'class' : 'form-control common-input-bkg'})
        self.fields['md_institucion'].widget = forms.TextInput(attrs={'class' : 'form-control common-input-bkg'})
    class Meta:
        model = Doctor
        fields = ("md_fullname", "md_specialize", "md_contactphone", "md_mail","md_address","md_institucion")


class TurnoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(TurnoForm,self).__init__(*args, **kwargs)
        self.fields['doctor'] = forms.ModelChoiceField(queryset=Doctor.objects.all(),
                                                         widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Turno
        fields = ("date", "place", "doctor")


class DoctorModalForm(BSModalModelForm):


    class Meta:
        model= Doctor
        fields = ("md_fullname", "md_specialize", "md_contactphone", "md_mail","md_address","md_institucion")
