from django.db import models
from django.urls import reverse
from login.models import CustomUser
from PIL import Image

# Create your models here.

class Doctor(models.Model):
    md_fullname = models.CharField(max_length=200, blank=True, null=True)
    md_specialize = models.CharField(max_length=100, blank=True, null=True)
    md_contactphone = models.CharField(max_length=20, blank=True, null=True)
    md_mail = models.EmailField(max_length=254, blank=True, null=True)
    md_address = models.CharField(max_length=500, blank=True, null=True)
    md_institucion = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null= True)

    def natural_key(self):
        return (self.md_fullname)

    def __str__(self):
        return self.md_fullname

    def get_absolute_url(self):
        return reverse("doctor_detail", kwargs={"pk": self.pk})


class Turno(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    place = models.CharField(max_length=500, blank=True, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Turno: {self.place}, User {self.user.email}"

    def get_absolute_url(self):
        return reverse("turno_detail", kwargs={"pk": self.pk})


class Receta(models.Model):
    prescription = models.CharField(max_length=100, blank=True, null=True)
    prescription_img = models.ImageField(upload_to="recetas_pics")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Prescription: {self.prescription}, User {self.user.email}"

    def get_absolute_url(self):
        return reverse("receta_detail", kwargs={"pk": self.pk})
    
    
    # def save(self):
    #     super().save()
    #     if self.prescription_img:
    #         prescription_img = Image.open(self.prescription_img.path)
    #         if prescription_img.height > 800 or prescription_img.width > 600:
    #             output_size = (800, 600)
    #             prescription_img.thumbnail(output_size)
    #             prescription_img.save(self.prescription_img.path)

    def save(self, *args, **kwargs):
        super().save()
        if self.prescription_img:
            img = Image.open(self.prescription_img.path)
            print("llego aca 4")
            if img.height > 200 or img.width > 200:
                new_img = (200, 200)
                img.thumbnail(new_img)
                img.save(self.prescription_img.path)



class Health(models.Model):
    CHOICE = (("si", "Sí"), ("no", "No"))
    height = models.FloatField()
    weight = models.FloatField()
    sedentary_work = models.CharField(
        max_length=3, choices=CHOICE, blank=True, null=True
    )
    smoker = models.CharField(max_length=3, choices=CHOICE, blank=True, null=True)
    insurance = models.CharField(max_length=100, blank=True, null=True)
    blood_type = models.CharField(max_length=5, blank=True, null=True)
    main_md = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING, blank=True, null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Health User: {self.user.email}"

    def get_absolute_url(self):
        return reverse("health_detail", kwargs={"pk": self.pk})


class Vacuna(models.Model):
    vax_name = models.CharField(max_length=50, blank=True, null=True)
    vax_desc = models.CharField(max_length=200, blank=True, null=True)
    user = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.vax_name


class Enf_Preexistentes(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    user = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.name
